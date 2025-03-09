#!/usr/bin/env python3
import csv
import logging

import psycopg2


class ScrappedDatabaseLoader:
    """
    ETL LOAD step that:
      1. Executes an external cleaning script.
      2. Reads cleaned CSV data.
      3. Connects to a PostgreSQL database.
      4. Updates the database in batches.
      5. Commits the transaction and closes the connection.
    """

    def __init__(self, csv_path: str, db_config: dict, batch_size: int = 500):
        """
        Initialize the DatabaseLoader.

        :param csv_path: Path to the CSV file.
        :param db_config: Dictionary with database connection parameters.
        :param batch_size: Number of records to process per batch.
        """
        self.csv_path = csv_path
        self.db_config = db_config
        self.batch_size = batch_size
        self.data = []
        self.conn = None
        self.cur = None

    def load_csv_data(self):
        """Read the CSV file into a list of dictionaries."""
        logging.info("Reading the CSV file...")
        with open(self.csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            self.data = list(reader)
        logging.info(f"Read {len(self.data)} records from the CSV file.")

    def connect_database(self):
        """Establish a connection to the PostgreSQL database."""
        logging.info("Connecting to the database...")
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_config.get("dbname"),
                user=self.db_config.get("user"),
                password=self.db_config.get("password"),
                host=self.db_config.get("host"),
                port=self.db_config.get("port"),
            )
            self.cur = self.conn.cursor()
            logging.info("Database connection established.")
        except Exception as e:
            logging.error(f"Error connecting to the database: {e}")
            raise e

    def batch_update(self):
        """Perform batch updates on the database."""
        update_query = """
        UPDATE companies
        SET 
            phone_number = COALESCE(NULLIF(%(phone_number)s, ''), phone_number),
            website = COALESCE(NULLIF(%(website)s, ''), website),
            reviews = CASE WHEN %(reviews)s = '' THEN reviews ELSE %(reviews)s END,
            schedule = CASE 
                        WHEN %(schedule)s = '' THEN schedule 
                        ELSE %(schedule)s::jsonb 
                    END,
            instagram = COALESCE(NULLIF(%(instagram)s, ''), instagram),
            facebook = COALESCE(NULLIF(%(facebook)s, ''), facebook),
            twitter = COALESCE(NULLIF(%(twitter)s, ''), twitter),
            linkedin = COALESCE(NULLIF(%(linkedin)s, ''), linkedin),
            youtube = COALESCE(NULLIF(%(youtube)s, ''), youtube),
            email = COALESCE(NULLIF(%(email)s, ''), email),
            scraping_date = NULLIF(%(scraping_date)s, '')::date
        WHERE siren_number = %(siren_number)s;
        """
        logging.info("Starting batch updates...")
        try:
            total_records = len(self.data)
            for i in range(0, total_records, self.batch_size):
                batch = self.data[i : i + self.batch_size]
                logging.info(
                    f"Processing batch {i // self.batch_size + 1} / { (total_records - 1) // self.batch_size + 1 }"
                )
                self.cur.executemany(update_query, batch)
        except Exception as e:
            logging.error(f"Error during batch updates: {e}")
            self.conn.rollback()
            raise e

    def commit_changes(self):
        """Commit the transaction to the database."""
        logging.info("Committing the changes to the database...")
        try:
            self.conn.commit()
        except Exception as e:
            logging.error(f"Error committing the changes: {e}")
            self.conn.rollback()
            raise e

    def close_connection(self):
        """Close the database cursor and connection."""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        logging.info("Database connection closed.")

    def run(self):
        """Run the full ETL LOAD process."""
        try:
            self.load_csv_data()
            self.connect_database()
            self.batch_update()
            self.commit_changes()
        finally:
            self.close_connection()
        logging.info("Script completed successfully.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    csv_path = "./InfoCompanies-Data-Model/fichier_combine_updated_big_fixed.csv"

    # Database configuration parameters
    db_config = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "root",
        "host": "localhost",
        "port": "5432",
    }

    loader = ScrappedDatabaseLoader(csv_path, db_config, batch_size=500)
    loader.run()

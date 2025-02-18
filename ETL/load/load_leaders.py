#!/usr/bin/env python3
import csv
import psycopg2
import logging
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class LeadersDBLoader:
    """
    ETL LOAD step for updating the 'leaders' table in PostgreSQL.
    It reads data from a CSV file, connects to the database, and performs
    batch updates using a parameterized query.
    """

    def __init__(self, csv_path: str, db_config: dict, batch_size: int = 100):
        """
        :param csv_path: Path to the Leaders CSV file.
        :param db_config: Dictionary containing database connection parameters.
        :param batch_size: Number of records to process per batch.
        """
        self.csv_path = csv_path
        self.db_config = db_config
        self.batch_size = batch_size
        self.data = []
        self.conn = None
        self.cur = None

    def load_csv(self):
        """Extract data from the CSV file."""
        logging.info("Loading the Leaders CSV file from %s...", self.csv_path)
        try:
            with open(self.csv_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile, delimiter=";")
                self.data = list(reader)
            logging.info("Loaded %d records from the CSV file.", len(self.data))
        except Exception as e:
            logging.error("Error reading CSV file: %s", e)
            sys.exit(1)

    def connect_db(self):
        """Connect to the PostgreSQL database."""
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
            logging.error("Error connecting to the database: %s", e)
            sys.exit(1)

    def batch_update(self):
        """Update the database in batches using a parameterized query."""
        update_query = """
        UPDATE leaders
        SET 
            role = COALESCE(NULLIF(%(role)s, ''), role),
            last_name = COALESCE(NULLIF(%(last_name)s, ''), last_name),
            first_name = COALESCE(NULLIF(%(first_name)s, ''), first_name),
            gestion_number = COALESCE(NULLIF(%(gestion_number)s, ''), gestion_number),
            type = COALESCE(NULLIF(%(type)s, ''), type),
            event_name = COALESCE(NULLIF(%(event_name)s, ''), event_name),
            greffe = COALESCE(NULLIF(%(greffe)s, ''), greffe),
            date_of_greffe = COALESCE(NULLIF(%(date_of_greffe)s, ''), date_of_greffe),
            usage_name = COALESCE(NULLIF(%(usage_name)s, ''), usage_name),
            pseudo = COALESCE(NULLIF(%(pseudo)s, ''), pseudo),
            company_name = COALESCE(NULLIF(%(company_name)s, ''), company_name),
            legal_form = COALESCE(NULLIF(%(legal_form)s, ''), legal_form),
            id_data = COALESCE(NULLIF(%(id_data)s, ''), id_data)
        WHERE siren = %(siren)s;
        """
        total_records = len(self.data)
        logging.info("Starting batch updates...")
        for i in range(0, total_records, self.batch_size):
            batch = self.data[i : i + self.batch_size]
            logging.info(
                "Processing batch %d / %d",
                i // self.batch_size + 1,
                (total_records - 1) // self.batch_size + 1,
            )
            try:
                self.cur.executemany(update_query, batch)
            except Exception as e:
                logging.error("Error during batch update: %s", e)
                self.conn.rollback()
                self.close_db()
                sys.exit(1)

    def commit_db(self):
        """Commit the changes to the database."""
        try:
            logging.info("Committing changes to the database...")
            self.conn.commit()
        except Exception as e:
            logging.error("Error committing changes: %s", e)
            self.conn.rollback()
            self.close_db()
            sys.exit(1)

    def close_db(self):
        """Close the database cursor and connection."""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        logging.info("Database connection closed.")

    def run(self):
        """Run the complete ETL LOAD process."""
        self.load_csv()
        self.connect_db()
        self.batch_update()
        self.commit_db()
        self.close_db()
        logging.info("Script completed successfully.")


if __name__ == "__main__":
    # Updated file path: Leaders CSV file
    csv_path = "./data/input/leaders.csv"  # Replace with the actual path

    # Database configuration parameters
    db_config = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "root",
        "host": "matithieu.com",
        "port": "5432",
    }

    # Batch update size can be adjusted as needed (default is 100)
    loader = LeadersDBLoader(csv_path, db_config, batch_size=100)
    loader.run()

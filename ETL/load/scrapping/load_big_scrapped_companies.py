#!/usr/bin/env python3
import logging
import os
import sys

import psycopg2

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class CompaniesDBLoader:
    """
    ETL LOAD step that:
      1. Connects to a PostgreSQL database.
      2. Creates a temporary table using the required schema.
      3. (Optionally) Removes specific lines from the CSV file.
      4. Imports CSV data into the temporary table.
      5. Updates the main table with data from the temporary table.
      6. Commits and closes the database connection.
    """

    def __init__(
        self,
        csv_file_path,
        main_table_name="companies",
        temp_table_name="temp_companies",
    ):
        self.csv_file_path = csv_file_path
        self.main_table_name = main_table_name
        self.temp_table_name = temp_table_name
        self.conn = None
        self.cur = None

    def connect_to_db(self):
        """Establish a connection to the PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "root"),
                dbname=os.getenv("DB_NAME", "postgres"),
            )
            self.cur = self.conn.cursor()
            logging.info("Database connection established.")
        except Exception as e:
            logging.error(f"Error connecting to the database: {e}")
            sys.exit(1)

    def copy_table_schema(self):
        """Create a temporary table with the required columns."""
        create_query = f"""
        CREATE TEMP TABLE {self.temp_table_name} (
            company_name TEXT,
            siren_number TEXT,
            nic_number TEXT,
            legal_form TEXT,
            ape_code TEXT,
            address TEXT,
            postal_code NUMERIC,
            city TEXT,
            region TEXT,
            registration_date DATE,
            deregistration_date DATE,

            closing_date_2018_1 DATE,
            revenue_2018_1 DOUBLE PRECISION,
            turnover_2018_1 DOUBLE PRECISION,
            closing_date_2018_2 DATE,
            revenue_2018_2 DOUBLE PRECISION,
            turnover_2018_2 DOUBLE PRECISION,
            closing_date_2018_3 DATE,
            revenue_2018_3 DOUBLE PRECISION,
            turnover_2018_3 DOUBLE PRECISION,

            closing_date_2019_1 DATE,
            revenue_2019_1 DOUBLE PRECISION,
            turnover_2019_1 DOUBLE PRECISION,
            closing_date_2019_2 DATE,
            revenue_2019_2 DOUBLE PRECISION,
            turnover_2019_2 DOUBLE PRECISION,
            closing_date_2019_3 DATE,
            revenue_2019_3 DOUBLE PRECISION,
            turnover_2019_3 DOUBLE PRECISION,

            closing_date_2020_1 DATE,
            revenue_2020_1 DOUBLE PRECISION,
            turnover_2020_1 DOUBLE PRECISION,
            closing_date_2020_2 DATE,
            revenue_2020_2 DOUBLE PRECISION,
            turnover_2020_2 DOUBLE PRECISION,
            closing_date_2020_3 DATE,
            revenue_2020_3 DOUBLE PRECISION,
            turnover_2020_3 DOUBLE PRECISION,

            closing_date_2021_1 DATE,
            revenue_2021_1 DOUBLE PRECISION,
            turnover_2021_1 DOUBLE PRECISION,
            closing_date_2021_2 DATE,
            revenue_2021_2 DOUBLE PRECISION,
            turnover_2021_2 DOUBLE PRECISION,
            closing_date_2021_3 DATE,
            revenue_2021_3 DOUBLE PRECISION,
            turnover_2021_3 DOUBLE PRECISION,

            closing_date_2022_1 DATE,
            revenue_2022_1 DOUBLE PRECISION,
            turnover_2022_1 DOUBLE PRECISION,
            closing_date_2022_2 DATE,
            revenue_2022_2 DOUBLE PRECISION,
            turnover_2022_2 DOUBLE PRECISION,
            closing_date_2022_3 DATE,
            revenue_2022_3 DOUBLE PRECISION,
            turnover_2022_3 DOUBLE PRECISION,
            
            industry_sector TEXT,
            phone_number TEXT,
            website TEXT,
            reviews JSONB,
            schedule JSONB,
            instagram TEXT,
            facebook TEXT,
            twitter TEXT,
            linkedin TEXT,
            youtube TEXT,
            email TEXT,
            scraping_date DATE
        );
        """
        try:
            self.cur.execute(create_query)
            logging.info(f"Temporary table `{self.temp_table_name}` created.")
        except Exception as e:
            logging.error(f"Error creating temporary table: {e}")
            sys.exit(1)

    def import_csv_to_temp_table(self):
        """Import CSV data into the temporary table using the COPY command."""
        try:
            with open(self.csv_file_path, "r", encoding="utf-8") as f:
                self.cur.copy_expert(
                    f"""
                    COPY {self.temp_table_name} 
                    FROM STDIN 
                    WITH CSV HEADER DELIMITER ';'
                    """,
                    f,
                )
            logging.info(f"CSV data imported into `{self.temp_table_name}`.")
        except Exception as e:
            logging.error(f"Error importing CSV: {e}")
            raise

    def update_main_table(self):
        """Update the main table with data from the temporary table."""
        try:
            update_query = f"""
            UPDATE {self.main_table_name} AS mt
            SET
                phone_number = COALESCE(NULLIF(tt.phone_number, ''), mt.phone_number),
                website = COALESCE(NULLIF(tt.website, ''), mt.website),
                reviews = CASE 
                            WHEN tt.schedule IS NULL THEN mt.reviews 
                            ELSE mt.reviews
                          END,
                schedule = CASE 
                            WHEN tt.schedule IS NULL THEN mt.schedule 
                            ELSE tt.schedule::jsonb 
                           END,
                instagram = COALESCE(NULLIF(tt.instagram, ''), mt.instagram),
                facebook = COALESCE(NULLIF(tt.facebook, ''), mt.facebook),
                twitter = COALESCE(NULLIF(tt.twitter, ''), mt.twitter),
                linkedin = COALESCE(NULLIF(tt.linkedin, ''), mt.linkedin),
                youtube = COALESCE(NULLIF(tt.youtube, ''), mt.youtube),
                email = COALESCE(NULLIF(tt.email, ''), mt.email),
                scraping_date = COALESCE(NULLIF(tt.scraping_date::text, '')::date, mt.scraping_date)
            FROM {self.temp_table_name} AS tt
            WHERE mt.siren_number = tt.siren_number;
            """
            self.cur.execute(update_query)
            logging.info(
                f"Main table `{self.main_table_name}` updated with data from `{self.temp_table_name}`."
            )
        except Exception as e:
            logging.error(f"Error updating main table: {e}")
            sys.exit(1)

    def remove_lines_from_csv(self, lines_to_remove):
        """
        Remove specific lines from the CSV file using sed.
        (This code is kept commented out as per instruction.)
        """
        # Uncomment the following lines if needed.
        # for line_number in lines_to_remove:
        #     try:
        #         if platform.system() == "Darwin":
        #             subprocess.run(["sed", "-i", "", f"{line_number}d", self.csv_file_path], check=True)
        #         else:
        #             subprocess.run(["sed", "-i", f"{line_number}d", self.csv_file_path], check=True)
        #         logging.info(f"Removed line {line_number} from CSV.")
        #     except Exception as e:
        #         logging.error(f"Error removing line {line_number}: {e}")
        pass

    def run(self):
        """Run the full ETL LOAD process."""
        self.connect_to_db()
        # Optional: Remove specified lines from the CSV file.
        # lines_to_remove = [1420697, 1481585, 1538082, 1672828, 1673548]
        # logging.info("Removing specified lines from the CSV file...")
        # self.remove_lines_from_csv(lines_to_remove)
        self.copy_table_schema()
        self.import_csv_to_temp_table()
        self.update_main_table()
        try:
            self.conn.commit()
            logging.info("Database changes committed.")
        except Exception as e:
            logging.error(f"Error committing changes: {e}")
            self.conn.rollback()
            sys.exit(1)
        finally:
            self.cur.close()
            self.conn.close()
            logging.info("Database connection closed.")


def main():
    # CSV file path from environment variable or default
    csv_file_path = os.getenv(
        "CSV_FILE_PATH",
        "./InfoCompanies-Data-Model/fichier_combine_updated_big_fixed.csv",
    )
    main_table_name = "companies"  # Main table name (as defined in your DB)
    temp_table_name = "temp_companies"  # Temporary table name

    loader = CompaniesDBLoader(csv_file_path, main_table_name, temp_table_name)
    loader.run()


if __name__ == "__main__":
    main()

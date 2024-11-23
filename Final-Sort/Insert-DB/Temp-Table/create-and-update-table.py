import psycopg2
import os
import subprocess
import platform
import sys

# Database configuration (replace with your actual values)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "postgres")
CSV_FILE_PATH = os.getenv(
    "CSV_FILE_PATH", "./InfoCompanies-Data-Model/fichier_combine_updated_big_fixed.csv"
)


def connect_to_db():
    """Establish a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME,
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        exit(1)


def copy_table_schema(cursor, temp_table_name):
    """Create a temporary table with the required columns."""
    cursor.execute(
        f"""
        CREATE TEMP TABLE {temp_table_name} (
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
    )
    print(f"Temporary table `{temp_table_name}` created.")


def import_csv_to_temp_table(cursor, temp_table_name, csv_file_path):
    """Import CSV data into the temporary table."""
    try:
        with open(csv_file_path, "r", encoding="utf-8") as f:
            cursor.copy_expert(
                f"""
                COPY {temp_table_name} 
                FROM STDIN 
                WITH CSV HEADER DELIMITER ';'
                """,
                f,
            )
        print(f"CSV data imported into `{temp_table_name}`.")
    except Exception as e:
        print(f"Error importing CSV: {e}")
        raise


def update_main_table(cursor, main_table_name, temp_table_name):
    """Update the main table with data from the temporary table."""
    cursor.execute(
        f"""
        UPDATE {main_table_name} AS mt
        SET
            phone_number = COALESCE(NULLIF(tt.phone_number, ''), mt.phone_number),
            website = COALESCE(NULLIF(tt.website, ''), mt.website),
            reviews = CASE 
                        WHEN tt.schedule IS NULL THEN mt.schedule 
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
        FROM {temp_table_name} AS tt
        WHERE mt.siren_number = tt.siren_number;
        """
    )
    print(f"`{main_table_name}` updated with data from `{temp_table_name}`.")


# Depending on the OS, the sed command may need to be adjusted
def remove_line_with_sed(line_number, file_path):
    system = platform.system()
    if system == "Darwin":
        # macOS
        subprocess.run(["sed", "-i", "", f"{line_number}d", file_path], check=True)
    else:
        # Linux (assumes GNU sed)
        subprocess.run(["sed", "-i", f"{line_number}d", file_path], check=True)


def main():
    # Table names
    main_table_name = "companies"  # Use exact table name as per your schema
    temp_table_name = "temp_companies"  # Temporary table name

    # Step 0: Remove the specified lines from the CSV file

    # lines_to_remove = [4204, 202711, 202738, 202767]
    # print("Removing specified lines from the CSV file...")
    # for line_number in lines_to_remove:
    #     remove_line_with_sed(line_number, CSV_FILE_PATH)

    # Connect to the database
    conn = connect_to_db()
    try:
        with conn:
            with conn.cursor() as cursor:
                # Step 1: Create a temporary table with the required columns
                print("Creating temporary table...")
                copy_table_schema(cursor, temp_table_name)

                # Step 2: Import CSV into the temporary table
                print("Importing CSV data into temporary table...")
                import_csv_to_temp_table(cursor, temp_table_name, CSV_FILE_PATH)

                # Step 3: Update the main table with data from the temporary table
                print("Updating main table...")
                update_main_table(cursor, main_table_name, temp_table_name)

                print("Database update process completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)  # Exit if error occurs
    finally:
        conn.close()


if __name__ == "__main__":
    main()

import csv
import psycopg2
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# DON'T FORGET TO CREATE THE INDEXES !!!

# Read the CSV file
data = []
csv_path = "./InfoCompanies-Data-Model/fichier_combine_updated.csv"
# csv_path = "/tmp/combine.csv"

logging.info("Reading the CSV file...")
with open(csv_path, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=";")
    data = list(reader)
logging.info(f"Read {len(data)} records from the CSV file.")

# Database connection
try:
    logging.info("Connecting to the database...")
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="root",
        host="localhost",
        port="5432",
    )
    logging.info("Database connection established.")
except Exception as e:
    logging.error(f"Error connecting to the database: {e}")
    exit(1)

# Prepare the cursor
cur = conn.cursor()

# Batch update size (adjust as needed)
batch_size = 500

try:
    logging.info("Starting batch updates...")
    for i in range(0, len(data), batch_size):
        batch = data[i : i + batch_size]
        logging.info(
            f"Processing batch {i // batch_size + 1} / {len(data) // batch_size + 1}"
        )

        update_query = """
        UPDATE companies
        SET 
            phone_number = COALESCE(NULLIF(%(phone_number)s, ''), phone_number),
            website = COALESCE(NULLIF(%(website)s, ''), website),
            reviews = CASE WHEN %(reviews)s = '' THEN reviews ELSE %(reviews)s END,
            schedule = COALESCE(NULLIF(%(schedule)s, ''), schedule),
            instagram = COALESCE(NULLIF(%(instagram)s, ''), instagram),
            facebook = COALESCE(NULLIF(%(facebook)s, ''), facebook),
            twitter = COALESCE(NULLIF(%(twitter)s, ''), twitter),
            linkedin = COALESCE(NULLIF(%(linkedin)s, ''), linkedin),
            youtube = COALESCE(NULLIF(%(youtube)s, ''), youtube),
            email = COALESCE(NULLIF(%(email)s, ''), email),
            scraping_date = NULLIF(%(scraping_date)s, '')::date
        WHERE siren_number = %(siren_number)s;
        """

        cur.executemany(update_query, batch)
except Exception as e:
    logging.error(f"Error during batch updates: {e}")
    conn.rollback()
    cur.close()
    conn.close()
    exit(1)

# Commit the changes to the database
try:
    logging.info("Committing the changes to the database...")
    conn.commit()
except Exception as e:
    logging.error(f"Error committing the changes: {e}")
    conn.rollback()
    cur.close()
    conn.close()
    exit(1)

# Close the cursor and connection
cur.close()
conn.close()
logging.info("Database connection closed.")
logging.info("Script completed successfully.")

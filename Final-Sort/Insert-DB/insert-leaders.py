import csv
import psycopg2
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Do not load the CSV, it will crash
# Read the CSV file
data = []
csv_path = ""

logging.info("Reading the Leaders CSV file...")
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
        host="matithieu.com",
        port="5432",
    )
    logging.info("Database connection established.")
except Exception as e:
    logging.error(f"Error connecting to the database: {e}")
    exit(1)

# Prepare the cursor
cur = conn.cursor()

# Batch update size (adjust as needed)
batch_size = 100

try:
    logging.info("Starting batch updates...")
    for i in range(0, len(data), batch_size):
        batch = data[i : i + batch_size]
        logging.info(
            f"Processing batch {i // batch_size + 1} / {len(data) // batch_size + 1}"
        )

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

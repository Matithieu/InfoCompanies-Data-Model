import csv
import json
import psycopg2

# Read the CSV file
data = []
csv_path = "./fichier_combine_updated.csv"
with open(csv_path, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=";")
    data = list(reader)

# Database connection
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="root",
    host="localhost",
    port="5432",
)

# Prepare the cursor
cur = conn.cursor()

# Batch update size (adjust as needed)
batch_size = 100

for i in range(0, len(data), batch_size):
    batch = data[i:i + batch_size]

    update_query = """
    UPDATE companies
    SET 
        phone = COALESCE(NULLIF(%(Phone)s, ''), phone),
        website = COALESCE(NULLIF(%(Website)s, ''), website),
        reviews = CASE WHEN %(Reviews)s = '' THEN reviews ELSE %(Reviews)s END,
        schedule = COALESCE(NULLIF(%(Schedule)s, ''), schedule),
        instagram = COALESCE(NULLIF(%(Instagram)s, ''), instagram),
        facebook = COALESCE(NULLIF(%(Facebook)s, ''), facebook),
        twitter = COALESCE(NULLIF(%(Twitter)s, ''), twitter),
        linkedin = COALESCE(NULLIF(%(LinkedIn)s, ''), linkedin),
        youtube = COALESCE(NULLIF(%(Youtube)s, ''), youtube),
        email = COALESCE(NULLIF(%(Email)s, ''), email),
        date_of_scrapping = %(DateOfScrapping)s
    WHERE siren = %(Siren)s;
    """

    cur.executemany(update_query, batch)

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

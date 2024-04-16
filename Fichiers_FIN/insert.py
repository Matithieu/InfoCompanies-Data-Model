import csv
import psycopg2

# DON'T FORGET TO CREATE THE INDEXES !!!

# Read the CSV file
data = []
csv_path = "./fichier_combine_updated.csv"
# csv_path = "/tmp/combine.csv"

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

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

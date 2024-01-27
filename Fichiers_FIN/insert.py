import csv
import json
import psycopg2

# Read the CSV file
data = []
csv_path = "./fichier_combine_updated.csv"
with open(csv_path, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=";")
    for row in reader:
        data.append(row)

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

for row in data:
    siren = row["Siren"]

    # Convert the dictionary strings to valid JSON format
    reviews_json = json.dumps(eval(row["Reviews"])) if row["Reviews"] else None
    schedule_json = json.dumps(eval(row["Schedule"])) if row["Schedule"] else None

    update_query = """
    UPDATE companies
    SET 
        phone = %s,
        website = %s,
        reviews = %s,
        schedule = %s,
        instagram = %s,
        facebook = %s,
        twitter = %s,
        linkedin = %s,
        youtube = %s,
        email = %s,
        date_of_scrapping = %s
    WHERE siren = %s;
    """

    cur.execute(
        update_query,
        (
            row["Phone"],
            row["Website"],
            reviews_json,
            schedule_json,
            row["Instagram"],
            row["Facebook"],
            row["Twitter"],
            row["LinkedIn"],
            row["Youtube"],
            row["Email"],
            row["DateOfScrapping"],
            siren,
        ),
    )

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
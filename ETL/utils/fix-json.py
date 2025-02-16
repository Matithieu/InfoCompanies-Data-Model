import csv
import json


# Function to validate and fix JSON strings
def fix_json(value):
    try:
        # Attempt to parse JSON
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        # If parsing fails, return an empty dictionary
        return {}


# Read and fix the CSV
def process_csv(input_file, output_file):
    with open(input_file, mode="r", encoding="utf-8") as infile, open(
        output_file, mode="w", encoding="utf-8", newline=""
    ) as outfile:
        reader = csv.DictReader(infile, delimiter=";")
        fieldnames = reader.fieldnames  # Read fieldnames from the input file
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()

        for row in reader:
            # Ensure the row has only valid fieldnames
            row = {key: row[key] for key in fieldnames if key in row}

            # Fix specific JSON fields
            row["reviews"] = fix_json(row.get("reviews", "{}"))
            row["schedule"] = fix_json(row.get("schedule", "{}"))

            # Convert JSON fields back to strings for writing
            row["reviews"] = json.dumps(row["reviews"], ensure_ascii=False)
            row["schedule"] = json.dumps(row["schedule"], ensure_ascii=False)

            writer.writerow(row)


# Input and output CSV file paths
input_csv = "./InfoCompanies-Data-Model/fichier_combine_updated_big.csv"  # Replace with your input file path
output_csv = "./InfoCompanies-Data-Model/fichier_combine_updated_big_fixed.csv"  # Replace with your output file path

# Process the CSV file
process_csv(input_csv, output_csv)
print(f"Fixed data written to {output_csv}")

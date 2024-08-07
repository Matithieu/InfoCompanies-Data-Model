import csv
import tempfile
import os

# Input file name
file_name = "leaders_renamed.csv"

# Create a temporary file
temp_file = tempfile.NamedTemporaryFile(
    mode="w", delete=False, newline="", encoding="utf-8"
)

# Read the input CSV file and write to the temporary file
with open(file_name, "r", newline="", encoding="utf-8") as infile, temp_file:
    reader = csv.reader(infile, delimiter=";")
    writer = csv.writer(temp_file, delimiter=";")

    # Read and write the header
    header = next(reader)
    writer.writerow(header)

    # Process each row
    for row in reader:
        # Remove '.0' from the siren column (first column)
        if row[0].endswith(".0"):
            row[0] = row[0][:-2]

        # Write the modified row to the temporary file
        writer.writerow(row)

# Close the temporary file
temp_file.close()

# Replace the original file with the temporary file
os.replace(temp_file.name, file_name)

print(f"Processing complete. File '{file_name}' has been updated.")

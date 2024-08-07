import csv
import tempfile
import os

# Input file name
file_name = "final.csv"

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

    # Find the index of the siren_number column
    siren_index = header.index("siren_number")

    # Process each row
    for row in reader:
        # Remove '.0' from the siren_number column
        if row[siren_index].endswith(".0"):
            row[siren_index] = row[siren_index][:-2]

        # Write the modified row to the temporary file
        writer.writerow(row)

# Close the temporary file
temp_file.close()

# Replace the original file with the temporary file
os.replace(temp_file.name, file_name)

print(f"Processing complete. File '{file_name}' has been updated.")

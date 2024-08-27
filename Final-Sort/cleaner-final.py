import csv
import tempfile
import os

# Input file name
file_name = "final.csv"


# Define your cleaning rules in a dictionary
# Key: column name; Value: cleaning function
def remove_decimal(value):
    if value.endswith(".0"):
        return value[:-2]
    return value


def clean_whitespace(value):
    return value.strip()


cleaning_rules = {
    "siren_number": remove_decimal,
    "number_of_employee": remove_decimal,  # You can add more columns and rules here
}

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

    # Create a map of column indices to cleaning functions
    column_cleaning_map = {
        header.index(col): func for col, func in cleaning_rules.items() if col in header
    }

    # Process each row
    for row in reader:
        # Apply the cleaning functions to the appropriate columns
        for col_index, cleaning_func in column_cleaning_map.items():
            row[col_index] = cleaning_func(row[col_index])

        # Write the modified row to the temporary file
        writer.writerow(row)

# Close the temporary file
temp_file.close()

# Replace the original file with the temporary file
os.replace(temp_file.name, file_name)

print(f"Processing complete. File '{file_name}' has been updated.")

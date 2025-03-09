import csv
import os
import re
import tempfile
import unicodedata


class FinalFileCleaner:
    """
    ETL process that cleans a CSV file by applying defined cleaning rules
    to specific columns. The process reads the input CSV, cleans each row,
    and then writes the result to an output CSV file.
    """

    def __init__(self, input_file: str, output_file: str, cleaning_rules: dict):
        """
        Initialize the file cleaner.

        :param input_file: Path to the input CSV file.
        :param output_file: Path to the output CSV file.
        :param cleaning_rules: Dictionary mapping column names to cleaning functions.
        """
        self.input_file = input_file
        self.output_file = output_file
        self.cleaning_rules = cleaning_rules

    def run(self):
        # Create a temporary file for output
        temp_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, newline="", encoding="utf-8"
        )

        # Open the input file and temporary file
        with open(
            self.input_file, "r", newline="", encoding="utf-8"
        ) as infile, temp_file as outfile:
            reader = csv.reader(infile, delimiter=";")
            writer = csv.writer(outfile, delimiter=";")

            # Read and write header
            header = next(reader)
            writer.writerow(header)

            # Map column indices to cleaning functions if the column exists in header
            column_cleaning_map = {
                header.index(col): func
                for col, func in self.cleaning_rules.items()
                if col in header
            }

            # Process each row and apply cleaning rules
            for row in reader:
                for col_index, cleaning_func in column_cleaning_map.items():
                    row[col_index] = cleaning_func(row[col_index])
                writer.writerow(row)

        # Close temporary file and replace the original file with the cleaned version
        temp_file.close()
        os.replace(temp_file.name, self.output_file)
        print(f"Processing complete. File '{self.output_file}' has been updated.")


def remove_trailing_dot_zero(value: str) -> str:
    """Remove trailing '.0' if present."""
    return value[:-2] if value.endswith(".0") else value


def standardize_text(value: str) -> str:
    """
    Cleans and standardizes text:
    - Trim whitespace and convert to lowercase
    - Normalize Unicode characters
    - Remove accents properly
    - Remove extra spaces
    - Capitalize first letter or each word
    """
    if not value:
        return ""

    # Normalize Unicode (NFKC helps with common encoding issues)
    value = unicodedata.normalize("NFKC", value).strip().lower()

    # Remove accents properly
    value = "".join(
        c
        for c in unicodedata.normalize("NFD", value)
        if unicodedata.category(c) != "Mn"
    )

    # Replace multiple spaces with a single space
    value = re.sub(r"\s+", " ", value)

    # Capitalize first letter of each word (optional)
    value = value.capitalize()  # Use value.title() if you want to capitalize every word

    return value


def clean_city_name(value: str) -> str:
    """
    Cleans and standardizes city names:
    - Removes leading numbers and special characters
    - Strips unwanted uppercase alphanumeric codes
    - Normalizes Unicode and removes accents
    - Trims spaces and capitalizes words properly
    """
    if not value:
        return ""

    # Normalize Unicode and trim
    value = unicodedata.normalize("NFKC", value).strip().lower()

    # Remove accents
    value = "".join(
        c
        for c in unicodedata.normalize("NFD", value)
        if unicodedata.category(c) != "Mn"
    )

    # Remove leading numbers, symbols, and unwanted characters
    value = re.sub(r"^[\W\d]+", "", value)

    # Remove standalone uppercase alphanumeric codes (like "A15", "A4971")
    value = re.sub(r"\b[A-Z0-9]{2,}\b", "", value).strip()

    # Replace multiple spaces with a single space
    value = re.sub(r"\s+", " ", value)

    # Capitalize first letter of each word
    value = value.title()

    return value if value else None  # Ensure empty strings are returned as None


if __name__ == "__main__":
    input_file = "./ETL/data/output/combine/fichier_effectif_and_combine.csv"
    output_file = "./ETL/data/output/final.csv"

    # Define the cleaning rules for various columns
    cleaning_rules = {
        "siren_number": remove_trailing_dot_zero,
        "nic_number": remove_trailing_dot_zero,
        "department_number": remove_trailing_dot_zero,
        "postal_code": remove_trailing_dot_zero,
        "number_of_employee": remove_trailing_dot_zero,
        "ape_label": standardize_text,
        "city": clean_city_name,
        "region": standardize_text,
        "industry_sector": standardize_text,
        "legal_form": standardize_text,
    }

    # Create and run the ETL pipeline
    cleaner = FinalFileCleaner(input_file, output_file, cleaning_rules)
    cleaner.run()

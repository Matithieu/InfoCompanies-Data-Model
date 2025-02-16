import csv
import tempfile
import os


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


if __name__ == "__main__":
    input_file = "./ETL/data/output/combine/fichier_effectif_and_combine.csv"
    output_file = "./ETL/data/output/final.csv"

    # Define cleaning rules:
    # For example, remove a trailing ".0" from the values in specified columns.
    def remove_trailing_dot_zero(value):
        return value[:-2] if value.endswith(".0") else value

    cleaning_rules = {
        "siren_number": remove_trailing_dot_zero,
        "nic_number": remove_trailing_dot_zero,
        "department_number": remove_trailing_dot_zero,
        "postal_code": remove_trailing_dot_zero,
        "number_of_employee": remove_trailing_dot_zero,
        # You can add more columns and corresponding cleaning functions here.
    }

    # Create and run the ETL pipeline
    cleaner = FinalFileCleaner(input_file, output_file, cleaning_rules)
    cleaner.run()


# to do: run the db script to see if the db is filled in meta

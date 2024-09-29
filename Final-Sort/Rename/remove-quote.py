import shutil


def find_column_indices(header, target_columns):
    header_parts = header.strip().split(";")
    column_indices = {}
    for col in target_columns:
        try:
            column_indices[col] = header_parts.index(col)
        except ValueError:
            print(f"Warning: Column '{col}' not found in the CSV header.")
    return column_indices


def replace_quotes(csv_line, column_indices):
    parts = csv_line.strip().split(";")
    for col, index in column_indices.items():
        if index < len(parts):
            parts[index] = parts[index].replace("'", '"')
    return ";".join(parts)


def process_csv_file(input_file, output_file):
    target_columns = ["reviews", "schedule"]

    with open(input_file, "r", encoding="utf-8") as infile, open(
        output_file, "w", encoding="utf-8"
    ) as outfile:
        # Process the header
        header = next(infile, None)
        if header is None:
            print("Error: Empty CSV file")
            return

        column_indices = find_column_indices(header, target_columns)
        outfile.write(header)  # Write the original header

        # Process the rest of the file
        for line in infile:
            processed_line = replace_quotes(line, column_indices)
            outfile.write(processed_line + "\n")


# Example usage
input_file = "./InfoCompanies-Data-Model/fichier_combine_updated.csv"
temp_output_file = "./InfoCompanies-Data-Model/temp_fichier_combine_updated.csv"

process_csv_file(input_file, temp_output_file)

# Replace the original file with the processed file
shutil.move(temp_output_file, input_file)

print(f"Processed CSV file has been saved to {input_file}")

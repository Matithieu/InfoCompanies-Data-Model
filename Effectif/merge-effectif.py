import pandas as pd
import numpy as np

# Parameters
path_file_effectif = "./fichier_effectif.csv"
input_file = "./fichier_renamed.csv"
output_file = "final.csv"
chunk_size = 100_000  # Adjust based on your memory capacity
# Count the total size of the cleaned file
with open(input_file, "r") as file:
    total_size = sum(1 for line in file) - 1  # Subtract 1 for the header
print("Total size of the cleaned file:", total_size)


# Initialize the array
array_siren_number = np.zeros(total_size, dtype=int)


def get_siren(chunk, count):
    if "siren_number" in chunk.columns:
        siren_values = chunk["siren_number"].astype(int).to_numpy()

        # Calculate the end index and ensure it does not exceed the array size
        end_index = count + len(siren_values)
        if end_index <= total_size:
            array_siren_number[count:end_index] = siren_values
        else:
            print("Warning: Exceeds total size.")

    else:
        print("Problem data, count =", count, "\n")

    # Update the count
    count += len(siren_values)
    return count


try:
    # Read CSV in chunks, only reading the 'siren_number' column
    chunks_template = pd.read_csv(
        input_file,
        chunksize=chunk_size,
        delimiter=";",
        usecols=["siren_number"],  # Only read the 'siren_number' column
        on_bad_lines="skip",
        low_memory=False,
    )

    count = 0  # Initialize count for indexing
    for chunk in chunks_template:
        count = get_siren(chunk, count)

except pd.errors.ParserError as e:
    print(f"Error reading CSV file: {e}")

# Print a part of the array to verify
# print("Type of array_siren_number:", type(array_siren_number))
# print("Type of array_siren_number[0]:", type(array_siren_number[0]))
# print(array_siren_number[:10])

# Convert array_siren_number to a set for faster lookups
array_siren_number_set = set(array_siren_number)

# Read the cleaned CSV file in chunks
chunks_cleaned = pd.read_csv(path_file_effectif, chunksize=chunk_size, low_memory=False)


def test_siren(chunk):
    if "siren" in chunk.columns:
        siren_values = chunk["siren"].astype(int).to_numpy()

        # Check if any siren_value is in array_siren_number_set
        matches = [siren for siren in siren_values if siren in array_siren_number_set]
        if matches:
            # print(f"Correspondance found for: {matches}")
            return chunk[chunk["siren"].isin(matches)]
        else:
            return pd.DataFrame()  # Return an empty DataFrame if no matches

    else:
        print("Error: 'siren' column not found in chunk")
        return pd.DataFrame()  # Return an empty DataFrame if no 'siren' column


# Initialize an empty list to collect matched DataFrames
matched_chunks = []

# Process each chunk
for chunk in chunks_cleaned:
    matched_chunk = test_siren(chunk)
    if not matched_chunk.empty:
        matched_chunks.append(matched_chunk)

# Concatenate all matched chunks into a single DataFrame
matched_data = pd.concat(matched_chunks, ignore_index=True)

# Load the template data
template_data = pd.read_csv(input_file, delimiter=";")

# Merge the matched data with the template data on 'siren_number' and 'siren'
merged_data = template_data.merge(
    matched_data, left_on="siren_number", right_on="siren", how="left"
)

# Drop the 'siren' column from the merged data
merged_data.drop("siren", axis=1, inplace=True)

# Save the merged data to a new CSV file
merged_data.to_csv(output_file, index=False, sep=";")

print("Merging complete. Output saved to:", output_file)

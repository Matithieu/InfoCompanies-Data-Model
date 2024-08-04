import pandas as pd


def process(chunk, columns_to_drop, columns_to_rename):
    # Remove the specified columns
    chunk = chunk.drop(columns=columns_to_drop)
    # Rename the specified columns
    chunk = chunk.rename(columns=columns_to_rename)
    return chunk


chunk_size = 100000  # Adjust this size based on your memory capacity
input_file = "./Effectif/StockUniteLegale_utf8.csv"
output_file = "fichier_effectif.csv"

# Initialize a flag to write the header only once
header_written = False

# Read the CSV file in chunks
chunks = pd.read_csv(input_file, chunksize=chunk_size, low_memory=False)

# Columns to drop
columns_to_drop = [
    "statutDiffusionUniteLegale",
    "unitePurgeeUniteLegale",
    "sigleUniteLegale",
    "sexeUniteLegale",
    "prenom1UniteLegale",
    "prenom2UniteLegale",
    "prenom3UniteLegale",
    "prenom4UniteLegale",
    "prenomUsuelUniteLegale",
    "pseudonymeUniteLegale",
    "identifiantAssociationUniteLegale",
    "trancheEffectifsUniteLegale",
    "anneeEffectifsUniteLegale",
    "anneeCategorieEntreprise",
    "dateDebut",
    "etatAdministratifUniteLegale",
    "nomUniteLegale",
    "nomUsageUniteLegale",
    "denominationUniteLegale",
    "denominationUsuelle1UniteLegale",
    "denominationUsuelle2UniteLegale",
    "denominationUsuelle3UniteLegale",
    "categorieJuridiqueUniteLegale",
    "activitePrincipaleUniteLegale",
    "nomenclatureActivitePrincipaleUniteLegale",
    "nicSiegeUniteLegale",
    "economieSocialeSolidaireUniteLegale",
    "societeMissionUniteLegale",
    "caractereEmployeurUniteLegale",
]

# Columns to rename
columns_to_rename = {
    "dateCreationUniteLegale": "date_creation",
    "dateDernierTraitementUniteLegale": "last_processing_date",
    "nombrePeriodesUniteLegale": "number_of_employee",
    "categorieEntreprise": "company_category",
}

# Initialize a counter for the chunks processed
chunk_counter = 0

# Process the CSV file in chunks
for chunk in chunks:

    # Increment the chunk counter
    chunk_counter += 1

    # Process the chunk to remove unwanted columns and rename columns
    processed_chunk = process(chunk, columns_to_drop, columns_to_rename)

    # Append the processed chunk to the new CSV file
    processed_chunk.to_csv(
        output_file, mode="a", header=not header_written, index=False
    )

    # Set header_written to True after the first chunk
    header_written = True

print(f"Processed file saved as {output_file}")

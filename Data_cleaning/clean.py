import pandas as pd

def process(chunk, columns_to_drop):
    # Remove the specified columns
    chunk = chunk.drop(columns=columns_to_drop)
    return chunk

chunk_size = 100000  # Adjust this size based on your memory capacity
input_file = 'StockUniteLegale_utf8.csv'
output_file = 'StockUniteLegale_cleaned.csv'

# Initialize a flag to write the header only once
header_written = False

# Read the CSV file in chunks
chunks = pd.read_csv(input_file, chunksize=chunk_size, low_memory=False)

# Columns to drop
columns_to_drop = [
    'statutDiffusionUniteLegale', 'unitePurgeeUniteLegale',
    'sigleUniteLegale', 'sexeUniteLegale', 'prenom1UniteLegale', 'prenom2UniteLegale', 'prenom3UniteLegale',
    'prenom4UniteLegale', 'prenomUsuelUniteLegale', 'pseudonymeUniteLegale', 'identifiantAssociationUniteLegale',
    'trancheEffectifsUniteLegale', 'anneeEffectifsUniteLegale',
    'anneeCategorieEntreprise', 'dateDebut', 'etatAdministratifUniteLegale', 'nomUniteLegale',
    'nomUsageUniteLegale', 'denominationUniteLegale', 'denominationUsuelle1UniteLegale', 'denominationUsuelle2UniteLegale',
    'denominationUsuelle3UniteLegale', 'categorieJuridiqueUniteLegale', 'activitePrincipaleUniteLegale',
    'nomenclatureActivitePrincipaleUniteLegale', 'nicSiegeUniteLegale', 'economieSocialeSolidaireUniteLegale',
    'societeMissionUniteLegale', 'caractereEmployeurUniteLegale'
]

# Initialize a counter for the chunks processed
chunk_counter = 0

# Process the CSV file in chunks
for chunk in chunks:

    # Increment the chunk counter
    chunk_counter += 1
    
    # Process the chunk to remove unwanted columns
    processed_chunk = process(chunk, columns_to_drop)
    
    # Append the processed chunk to the new CSV file
    processed_chunk.to_csv(output_file, mode='a', header=not header_written, index=False)
    
    # Set header_written to True after the first chunk
    header_written = True

print(f"Processed file saved as {output_file}")

import os
import pandas as pd


# Link: https://files.data.gouv.fr/insee-sirene/StockUniteLegale_utf8.zip
class StockUniteLegaleETL:
    """
    ETL pipeline for processing the StockUniteLegale CSV file in chunks.
    It extracts data from the input file, transforms it by dropping and renaming specified columns,
    and then loads the processed data into an output CSV file.
    """

    def __init__(self, input_file: str, output_file: str, chunk_size: int = 100_000):
        """
        Initialize the ETL pipeline.

        :param input_file: Path to the input CSV file.
        :param output_file: Path to the output CSV file.
        :param chunk_size: Number of rows per chunk.
        """
        self.input_file = input_file
        self.output_file = output_file
        self.chunk_size = chunk_size
        self.columns_to_drop = [
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
        self.columns_to_rename = {
            "dateCreationUniteLegale": "date_creation",
            "dateDernierTraitementUniteLegale": "last_processing_date",
            "nombrePeriodesUniteLegale": "number_of_employee",
            "categorieEntreprise": "company_category",
        }

    def extract(self):
        """
        Extract data from the input CSV file in chunks.
        Handles potential delimiter and quoting issues.

        :return: An iterator of DataFrame chunks.
        """
        return pd.read_csv(
            self.input_file,
            chunksize=self.chunk_size,
            sep=",",  # Ensure correct delimiter
            quotechar='"',  # Handle quoted fields properly
            low_memory=False,
            # on_bad_lines="skip",  # Skip bad lines
        )

    def transform(self, chunk: pd.DataFrame) -> pd.DataFrame:
        """
        Transform a chunk by dropping unwanted columns and renaming specified columns.

        :param chunk: Input DataFrame chunk.
        :return: Transformed DataFrame chunk.
        """
        # Drop unwanted columns (ignore if a column doesn't exist)
        chunk = chunk.drop(columns=self.columns_to_drop, errors="ignore")
        # Rename columns according to the mapping
        chunk = chunk.rename(columns=self.columns_to_rename)
        return chunk

    def load(self, transformed_chunk: pd.DataFrame, header: bool):
        """
        Load a transformed chunk into the output CSV file.

        :param transformed_chunk: The transformed DataFrame chunk.
        :param header: Boolean indicating whether to write the header.
        """
        # Ensure the output directory exists
        output_dir = os.path.dirname(self.output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        transformed_chunk.to_csv(
            self.output_file, mode="a", header=header, index=False, sep=";"
        )

    def run(self):
        """
        Run the full ETL process: Extract, Transform, and Load.
        """
        header_written = False
        chunk_counter = 0

        for chunk in self.extract():
            chunk_counter += 1
            transformed_chunk = self.transform(chunk)
            self.load(transformed_chunk, header=not header_written)
            header_written = True

        print(f"Processed file saved as {self.output_file}")


if __name__ == "__main__":
    input_file = "./ETL/data/input/effectif/stock_unite_legale.csv"
    output_file = "./ETL/data/output/extract/stock_unite_legale.csv"

    etl_pipeline = StockUniteLegaleETL(
        input_file=input_file, output_file=output_file, chunk_size=300_000
    )
    etl_pipeline.run()

    print("ETL StockUniteLegale process completed.")

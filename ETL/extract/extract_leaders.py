import os
import pandas as pd


class LeadersETL:
    """
    ETL process for the Leaders CSV file:
      - Extract: Reads the file in chunks while keeping specified columns.
      - Transform: Concatenates all chunks (transformation step could be expanded if needed).
      - Load: Writes the final DataFrame to the output CSV file.
    """

    def __init__(
        self,
        input_file: str,
        output_file: str,
        columns_to_keep: list,
        chunk_size: int = 500_000,
    ):
        """
        Initialize the ETL process.

        :param input_file: Path to the input CSV file.
        :param output_file: Path to the output CSV file.
        :param columns_to_keep: List of columns to load from the input file.
        :param chunk_size: Number of rows to process per chunk.
        """
        self.input_file = input_file
        self.output_file = output_file
        self.columns_to_keep = columns_to_keep
        self.chunk_size = chunk_size

    def extract(self) -> list:
        """
        Extract data from the input CSV file in chunks.

        :return: List of DataFrame chunks.
        """
        print(f"Extracting data from {self.input_file} in chunks...")
        chunks = []
        for chunk in pd.read_csv(
            self.input_file,
            sep=";",
            usecols=self.columns_to_keep,
            chunksize=self.chunk_size,
            low_memory=False,
        ):
            chunks.append(chunk)
        print(f"Extracted {len(chunks)} chunks.")
        return chunks

    def transform(self, chunks: list) -> pd.DataFrame:
        """
        Transform the extracted chunks by concatenating them.

        :param chunks: List of DataFrame chunks.
        :return: A single concatenated DataFrame.
        """
        print("Transforming data by concatenating chunks...")
        data = pd.concat(chunks, ignore_index=True)
        return data

    def load(self, data: pd.DataFrame):
        """
        Load the transformed data into the output CSV file.

        :param data: The DataFrame to be saved.
        """
        # Ensure the output directory exists
        output_dir = os.path.dirname(self.output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        data.to_csv(self.output_file, sep=";", index=False)
        print(f"Data successfully saved to {self.output_file}")

    def run(self):
        """
        Run the full ETL pipeline.
        """
        chunks = self.extract()
        data = self.transform(chunks)
        self.load(data)


if __name__ == "__main__":
    input_file = "./ETL/data/input/leaders/leaders.csv"
    output_file = "./ETL/data/output/extract/leaders.csv"

    # Columns to keep from the input file
    columns_to_keep = [
        "Siren",
        "Qualité",
        "Nom Patronymique",
        "Prénoms",
        "Numéro de Gestion",
        "Type",
        "Libellé Evènement",
        "Nom d'usage",
        "Pseudonyme",
        "Dénomination",
        "Forme_Juridique",
        "id",
    ]

    etl_pipeline = LeadersETL(
        input_file, output_file, columns_to_keep, chunk_size=500_000
    )
    etl_pipeline.run()

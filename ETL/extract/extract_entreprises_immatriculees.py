import glob
import os

import pandas as pd


# Link: https://opendata.datainfogreffe.fr/explore/?sort=modified&refine.theme=Immatriculations
class EntreprisesImmatriculeesETL:
    """
    A class to perform the ETL process for "entreprises immatriculees" CSV files.
    It loads files matching a pattern, selects specified columns, concatenates the data,
    and saves the final output to a CSV file.
    """

    def __init__(
        self,
        input_dir: str,
        file_pattern: str,
        columns_to_keep: list,
        output_dir: str,
        output_filename: str,
    ):
        """
        Initialize the ETL instance.

        :param input_dir: Directory where the input CSV files are stored.
        :param file_pattern: Pattern to match the CSV files (e.g., "entreprises-immatriculees-en-*.csv").
        :param columns_to_keep: List of columns to extract from the CSV files.
        :param output_dir: Directory where the output CSV file will be saved.
        :param output_filename: Name of the output CSV file.
        """
        self.input_dir = input_dir
        self.file_pattern = file_pattern
        self.columns_to_keep = columns_to_keep
        self.output_dir = output_dir
        self.output_filename = output_filename
        self.full_pattern = os.path.join(self.input_dir, self.file_pattern)
        self.frames = []

    def load_data(self):
        """
        Load CSV files matching the pattern and select the specified columns.
        """
        file_paths = glob.glob(self.full_pattern)
        if not file_paths:
            print("No files found matching the pattern:", self.full_pattern)
            return

        for path in file_paths:
            print(f"Loading file {path}...")
            try:
                df = pd.read_csv(
                    path, sep=";", usecols=self.columns_to_keep, low_memory=False
                )
                self.frames.append(df)
            except Exception as e:
                print(f"Error loading file {path}: {e}")

    def combine_data(self) -> pd.DataFrame:
        """
        Concatenate all loaded DataFrames into one DataFrame.

        :return: The combined DataFrame.
        """
        if not self.frames:
            print("No data frames loaded, returning an empty DataFrame.")
            return pd.DataFrame()
        return pd.concat(self.frames, ignore_index=True)

    def save_data(self, df: pd.DataFrame):
        """
        Save the combined DataFrame to a CSV file.

        :param df: The DataFrame to save.
        """
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        output_path = os.path.join(self.output_dir, self.output_filename)
        df.to_csv(output_path, sep=";", index=False)
        print(f"Combined CSV file saved as: {output_path}")


if __name__ == "__main__":
    # Configuration parameters

    input_directory = "./ETL/data/input/entreprises_immatriculees"
    file_pattern = "entreprises-immatriculees-en-*.csv"

    # Define the columns to keep from the CSV files
    columns_to_keep = [
        "Dénomination",
        "Siren",
        "Nic",
        "Forme Juridique",
        "Code APE",
        "Secteur d'activité",
        "Adresse",
        "Code postal",
        "Ville",
        "Région",
        "Nom commercial",
        "Date immatriculation",
        "Date radiation",
    ]

    output_directory = "./ETL/data/output/extract"
    output_file = "entreprises_immatriculees.csv"

    # Instantiate and run the ETL process
    etl = EntreprisesImmatriculeesETL(
        input_dir=input_directory,
        file_pattern=file_pattern,
        columns_to_keep=columns_to_keep,
        output_dir=output_directory,
        output_filename=output_file,
    )

    etl.load_data()
    combined_df = etl.combine_data()
    etl.save_data(combined_df)

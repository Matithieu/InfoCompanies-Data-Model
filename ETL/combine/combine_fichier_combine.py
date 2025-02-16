import os
import pandas as pd


class CombineFilesETL:
    """
    ETL class to combine multiple CSV files, clean the 'Siren' column,
    remove duplicates, and save the result to a new CSV file.
    """

    def __init__(self, input_files: list, output_file: str):
        """
        Initialize the ETL pipeline with input files and output file.

        :param input_files: List of CSV file paths to process.
        :param output_file: Path to the output CSV file.
        """
        self.input_files = input_files
        self.output_file = output_file

    def clean_siren_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the 'Siren' column by ensuring it contains only digits,
        converting it to a numeric type with missing values properly handled.

        :param df: DataFrame containing the 'Siren' column.
        :return: DataFrame with the cleaned 'Siren' column.
        """
        # Ensure the 'Siren' column is treated as a string and remove non-digit characters
        df["Siren"] = df["Siren"].astype(str).str.replace(r"\D", "", regex=True)
        # Convert cleaned values to numeric, coercing errors to NaN, then to nullable integer type
        df["Siren"] = pd.to_numeric(df["Siren"], errors="coerce").astype("Int64")
        return df

    def extract(self) -> list:
        """
        Extracts data from all input files.

        :return: List of DataFrames read from the input CSV files.
        """
        data_frames = []
        for file in self.input_files:
            print(f"Loading file {file}...")
            df = pd.read_csv(file, sep=";", low_memory=False)
            data_frames.append(df)
        return data_frames

    def transform(self, data_frames: list) -> pd.DataFrame:
        """
        Transforms the list of DataFrames by cleaning the 'Siren' column,
        concatenating them, and removing duplicate entries.

        :param data_frames: List of DataFrames to process.
        :return: A single combined and cleaned DataFrame.
        """
        processed_frames = []
        for i, df in enumerate(data_frames):
            df = self.clean_siren_column(df)
            if df["Siren"].isnull().any():
                print(f"Invalid Siren values found in file {self.input_files[i]}:")
                print(df[df["Siren"].isnull()])
            processed_frames.append(df)

        # Concatenate all DataFrames and remove duplicates based on 'Siren'
        combined_df = pd.concat(processed_frames, ignore_index=True, sort=False)
        combined_df = combined_df.drop_duplicates(subset=["Siren"])
        return combined_df

    def load(self, df: pd.DataFrame):
        """
        Loads the cleaned DataFrame to the output CSV file.

        :param df: The DataFrame to save.
        """
        # Ensure the output directory exists
        output_dir = os.path.dirname(self.output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        df.to_csv(self.output_file, sep=";", index=False)
        print(f"Combined data saved to {self.output_file}")

    def run(self):
        """
        Run the full ETL pipeline: Extract, Transform, and Load.
        """
        data_frames = self.extract()
        combined_df = self.transform(data_frames)
        self.load(combined_df)


if __name__ == "__main__":
    input_files = [
        "./ETL/data/output/transform/chiffres_cles.csv",
        "./ETL/data/output/transform/entreprises_immatriculees.csv",
        "./ETL/data/output/transform/entreprises_radiees.csv",
    ]
    output_file = "./ETL/data/output/combine/fichier_combine.csv"

    etl_pipeline = CombineFilesETL(input_files, output_file)
    etl_pipeline.run()

    print("ETL combine_files.py executed successfully.")

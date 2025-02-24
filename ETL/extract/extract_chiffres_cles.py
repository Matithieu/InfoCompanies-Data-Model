import os
import pandas as pd


# Link: https://opendata.datainfogreffe.fr/explore/?sort=modified&refine.theme=Chiffres+cles
class ChiffresClesETL:
    """
    A class to perform the ETL process on 'chiffres-cles' CSV files.
    It loads CSVs for multiple years, renames financial columns by appending the year,
    merges them based on the 'Siren' column, and saves the combined data.
    """

    def __init__(
        self,
        input_dir: str,
        file_prefix: str,
        years: list,
        output_dir: str,
        output_filename: str,
        columns_to_keep: list,
    ):
        """
        Initialize the ETL instance.

        :param input_dir: Directory where input CSV files are stored.
        :param file_prefix: Common prefix for the CSV file names.
        :param years: List of years (as strings) to process.
        :param output_dir: Directory where the output CSV will be saved.
        :param output_filename: Name of the output CSV file.
        :param columns_to_keep: List of columns to read from the CSV files.
        """
        self.input_dir = input_dir
        self.file_prefix = file_prefix
        self.years = years
        self.output_dir = output_dir
        self.output_filename = output_filename
        self.columns_to_keep = columns_to_keep
        self.data_frames = {}

    def _get_file_path(self, year: str) -> str:
        """
        Build the file path for a given year.

        :param year: Year as a string.
        :return: Full file path.
        """
        filename = f"{self.file_prefix}{year}.csv"
        return os.path.join(self.input_dir, filename)

    def load_data(self):
        """
        Load CSV files for each year, perform necessary transformations,
        and store them in a dictionary keyed by year.
        """
        for year in self.years:
            file_path = self._get_file_path(year)
            print(f"Loading file {file_path}...")
            try:
                data = pd.read_csv(
                    file_path, sep=";", usecols=self.columns_to_keep, low_memory=False
                )
            except Exception as e:
                print(f"Error loading file for year {year}: {e}")
                continue

            # Ensure that 'Siren' is treated as a string
            data["Siren"] = data["Siren"].astype(str)

            # Identify financial columns and rename them by appending the year
            financial_columns = [
                col
                for col in data.columns
                if col.startswith(("Date de cloture ", "CA ", "Résultat "))
            ]
            data.rename(
                columns={col: f"{col} - {year}" for col in financial_columns},
                inplace=True,
            )

            self.data_frames[year] = data

    def merge_data_frames(self) -> pd.DataFrame:
        """
        Merge all loaded DataFrames on the 'Siren' column.

        :return: The combined DataFrame.
        """
        combined_data = pd.DataFrame()
        for year, data in self.data_frames.items():
            if combined_data.empty:
                combined_data = data
            else:
                combined_data = pd.merge(
                    combined_data, data, on="Siren", how="left", suffixes=("", "_y")
                )

        # Remove any duplicate columns (those ending with '_y')
        combined_data = combined_data.loc[:, ~combined_data.columns.str.endswith("_y")]
        # Drop duplicates based on 'Siren'
        combined_data = combined_data.drop_duplicates(subset=["Siren"])
        return combined_data

    def save_data(self, dataframe: pd.DataFrame):
        """
        Save the combined DataFrame to a CSV file.

        :param dataframe: The DataFrame to save.
        """
        # Create the output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        output_path = os.path.join(self.output_dir, self.output_filename)
        dataframe.to_csv(output_path, index=False, sep=";")
        print(f"Combined CSV file has been saved as '{output_path}'.")


if __name__ == "__main__":
    # Configuration parameters

    input_directory = "./ETL/data/input/chiffres_cles"
    file_prefix = "chiffres-cles-"
    years = ["2020", "2021", "2022", "2023"]
    # years = ["2022", "2023"]

    output_directory = "./ETL/data/output/extract"
    output_file = "chiffres_cles.csv"

    columns_to_keep = [
        "Dénomination",
        "Siren",
        "Nic",
        "Forme Juridique",
        "Code APE",
        "Libellé APE",
        "Adresse",
        "Code postal",
        "Num. dept.",
        "Département",
        "Ville",
        "Région",
        "Date immatriculation",
        "Date radiation",
        "Date de cloture exercice 1",
        "CA 1",
        "Résultat 1",
        "Date de cloture exercice 2",
        "CA 2",
        "Résultat 2",
        "Date de cloture exercice 3",
        "CA 3",
        "Résultat 3",
    ]

    # Instantiate and run the ETL process
    etl_process = ChiffresClesETL(
        input_dir=input_directory,
        file_prefix=file_prefix,
        years=years,
        output_dir=output_directory,
        output_filename=output_file,
        columns_to_keep=columns_to_keep,
    )

    etl_process.load_data()
    combined_df = etl_process.merge_data_frames()
    etl_process.save_data(combined_df)

import os

import pandas as pd


class RenameAndAddColumnsETL:
    """
    ETL process that first adds missing columns and then renames columns
    using a translation dictionary.
    """

    def __init__(self, input_file: str, output_file: str):
        """
        Initialize the ETL process with input and output file paths.

        :param input_file: Path to the input CSV file.
        :param output_file: Path to the output CSV file.
        """
        self.input_file = input_file
        self.output_file = output_file

        # List of new columns to add if they are missing (using the final names)
        self.new_columns = [
            "phone_number",
            "website",
            "reviews",
            "schedule",
            "instagram",
            "facebook",
            "twitter",
            "linkedin",
            "youtube",
            "email",
            "scraping_date",
        ]

        # TODO: Add a migration tool in order to avoid dumping the database every time
        #
        # If adding new columns, please add also in the load_companies.py file
        # And add the columns in the InfoCompanies-API companies's model

        # Translation dictionary to rename headers
        self.translation_dict = {
            "Dénomination": "company_name",
            "Siren": "siren_number",
            "Nic": "nic_number",
            "Forme Juridique": "legal_form",
            "Code APE": "ape_code",
            "Libellé APE": "ape_label",
            "Adresse": "address",
            "Code postal": "postal_code",
            "Num. dept.": "department_number",
            "Département": "department",
            "Ville": "city",
            "Région": "region",
            "Nom commercial": "trade_name",
            "Date immatriculation": "registration_date",
            "Date radiation": "deregistration_date",
            #
            "Date de cloture exercice 1 - 2018": "closing_date_2018_1",
            "CA 1 - 2018": "revenue_2018_1",
            "Résultat 1 - 2018": "turnover_2018_1",
            "Date de cloture exercice 2 - 2018": "closing_date_2018_2",
            "CA 2 - 2018": "revenue_2018_2",
            "Résultat 2 - 2018": "turnover_2018_2",
            "Date de cloture exercice 3 - 2018": "closing_date_2018_3",
            "CA 3 - 2018": "revenue_2018_3",
            "Résultat 3 - 2018": "turnover_2018_3",
            #
            "Date de cloture exercice 1 - 2019": "closing_date_2019_1",
            "CA 1 - 2019": "revenue_2019_1",
            "Résultat 1 - 2019": "turnover_2019_1",
            "Date de cloture exercice 2 - 2019": "closing_date_2019_2",
            "CA 2 - 2019": "revenue_2019_2",
            "Résultat 2 - 2019": "turnover_2019_2",
            "Date de cloture exercice 3 - 2019": "closing_date_2019_3",
            "CA 3 - 2019": "revenue_2019_3",
            "Résultat 3 - 2019": "turnover_2019_3",
            #
            "Date de cloture exercice 1 - 2020": "closing_date_2020_1",
            "CA 1 - 2020": "revenue_2020_1",
            "Résultat 1 - 2020": "turnover_2020_1",
            "Date de cloture exercice 2 - 2020": "closing_date_2020_2",
            "CA 2 - 2020": "revenue_2020_2",
            "Résultat 2 - 2020": "turnover_2020_2",
            "Date de cloture exercice 3 - 2020": "closing_date_2020_3",
            "CA 3 - 2020": "revenue_2020_3",
            "Résultat 3 - 2020": "turnover_2020_3",
            #
            "Date de cloture exercice 1 - 2021": "closing_date_2021_1",
            "CA 1 - 2021": "revenue_2021_1",
            "Résultat 1 - 2021": "turnover_2021_1",
            "Date de cloture exercice 2 - 2021": "closing_date_2021_2",
            "CA 2 - 2021": "revenue_2021_2",
            "Résultat 2 - 2021": "turnover_2021_2",
            "Date de cloture exercice 3 - 2021": "closing_date_2021_3",
            "CA 3 - 2021": "revenue_2021_3",
            "Résultat 3 - 2021": "turnover_2021_3",
            #
            "Date de cloture exercice 1 - 2022": "closing_date_2022_1",
            "CA 1 - 2022": "revenue_2022_1",
            "Résultat 1 - 2022": "turnover_2022_1",
            "Date de cloture exercice 2 - 2022": "closing_date_2022_2",
            "CA 2 - 2022": "revenue_2022_2",
            "Résultat 2 - 2022": "turnover_2022_2",
            "Date de cloture exercice 3 - 2022": "closing_date_2022_3",
            "CA 3 - 2022": "revenue_2022_3",
            "Résultat 3 - 2022": "turnover_2022_3",
            #
            "Date de cloture exercice 1 - 2023": "closing_date_2023_1",
            "CA 1 - 2023": "revenue_2023_1",
            "Résultat 1 - 2023": "turnover_2023_1",
            "Date de cloture exercice 2 - 2023": "closing_date_2023_2",
            "CA 2 - 2023": "revenue_2023_2",
            "Résultat 2 - 2023": "turnover_2023_2",
            "Date de cloture exercice 3 - 2023": "closing_date_2023_3",
            "CA 3 - 2023": "revenue_2023_3",
            "Résultat 3 - 2023": "turnover_2023_3",
            #
            "Secteur d'activité": "industry_sector",
            "phone": "phone_number",
            "website": "website",
            "reviews": "reviews",
            "schedule": "schedule",
            "instagram": "instagram",
            "facebook": "facebook",
            "twitter": "twitter",
            "linkedin": "linkedin",
            "youtube": "youtube",
            "email": "email",
            "Phone": "phone_number",
            "Website": "website",
            "Reviews": "reviews",
            "Schedule": "schedule",
            "Instagram": "instagram",
            "Facebook": "facebook",
            "Twitter": "twitter",
            "LinkedIn": "linkedin",
            "Youtube": "youtube",
            "Email": "email",
            "DateOfScrapping": "scraping_date",
        }

    def extract(self) -> pd.DataFrame:
        """
        Extract the data from the input CSV file.
        """
        df = pd.read_csv(self.input_file, delimiter=";", low_memory=False)
        return df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform the DataFrame by adding missing columns first and then renaming the columns.
        """
        # First, add any missing new columns (using final column names)
        for col in self.new_columns:
            if col not in df.columns:
                df[col] = None

        # Then rename the columns using the translation dictionary
        df = df.rename(columns=self.translation_dict)
        return df

    def load(self, df: pd.DataFrame):
        """
        Load the transformed DataFrame into the output CSV file.
        """
        # Ensure the output directory exists
        output_dir = os.path.dirname(self.output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        df.to_csv(self.output_file, index=False, sep=";")
        print(f"File saved as {self.output_file}")

    def run(self):
        """
        Run the full ETL process: Extract, Transform, and Load.
        """
        df = self.extract()
        df = self.transform(df)
        self.load(df)


if __name__ == "__main__":
    input_file = "./ETL/data/output/combine/fichier_combine.csv"
    output_file = "./ETL/data/output/transform/fichier_combine.csv"

    etl_pipeline = RenameAndAddColumnsETL(input_file, output_file)
    etl_pipeline.run()

print("ETL transformation fichier_combine complete.")

import os

import pandas as pd


class LeadersRenameTransformation:
    """
    Transformation step to rename columns of the Leaders CSV file.

    It reads the sorted CSV file, renames the headers according to a translation dictionary,
    and writes the transformed file to the output path.
    """

    def __init__(self, input_file: str, output_file: str, translation_dict: dict):
        """
        Initialize the transformation.

        :param input_file: Path to the input CSV file (sorted file).
        :param output_file: Path to the output CSV file (renamed file).
        :param translation_dict: Dictionary mapping old column names to new names.
        """
        self.input_file = input_file
        self.output_file = output_file
        self.translation_dict = translation_dict

    def transform(self):
        print("Loading Leaders CSV for renaming from:", self.input_file)
        # Read the CSV into a DataFrame
        df = pd.read_csv(self.input_file, delimiter=";", encoding="utf-8")

        print("Renaming columns using the translation dictionary...")
        # Rename columns using the translation dictionary
        df.rename(columns=self.translation_dict, inplace=True)

        # Ensure the output directory exists
        output_dir = os.path.dirname(self.output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Write the transformed DataFrame to the output CSV
        df.to_csv(self.output_file, sep=";", index=False, encoding="utf-8")
        print("Leaders renaming done! Output saved to:", self.output_file)


if __name__ == "__main__":
    input_file = "./ETL/data/input/extract/leaders.csv"
    output_file = "./ETL/data/output/transform/leaders.csv"

    # Translation dictionary for renaming the headers
    translation_dict = {
        "Siren": "siren",
        "Qualité": "role",
        "Nom Patronymique": "last_name",
        "Prénoms": "first_name",
        "Numéro de Gestion": "gestion_number",
        "Type": "type",
        "Libellé Evènement": "event_name",
        "Nom d'usage": "usage_name",
        "Pseudonyme": "pseudo",
        "Dénomination": "company_name",
        "Forme_Juridique": "legal_form",
        "id": "id_data",
    }

    # Run the transformation step
    transformer = LeadersRenameTransformation(input_file, output_file, translation_dict)
    transformer.transform()

import pandas as pd
import numpy as np


def clean_entreprises_radiees(input_file: str, output_file: str):
    # Load the CSV file with a semicolon as the delimiter
    df = pd.read_csv(input_file, sep=";", low_memory=False)

    # Replace empty strings (or strings with only whitespace) with NaN
    df.replace(r"^\s*$", np.nan, regex=True, inplace=True)

    # --- Clean Identifier Columns ---
    # Convert 'Siren' to string and trim any whitespace
    if "Siren" in df.columns:
        df["Siren"] = df["Siren"].astype(str).str.strip()

    # Convert 'Nic' to string, remove trailing decimal (e.g. "10.0" -> "10")
    if "Nic" in df.columns:
        df["Nic"] = df["Nic"].astype(str).str.split(".").str[0].str.strip()

    # --- Clean Postal Code ---
    # Convert 'Code postal' to string and remove trailing ".0" if present
    if "Code postal" in df.columns:
        df["Code postal"] = (
            df["Code postal"]
            .astype(str)
            .str.strip()
            .replace(
                r"^\.$", "", regex=True
            )  # Si la valeur est exactement ".", on la remplace par ""
            .str.replace(r"\.0$", "", regex=True)  # Enlever le .0 en fin de chaîne
            .apply(
                lambda x: x if x.isdigit() else ""
            )  # Si le résultat n'est pas numérique, on le vide
        )

    # --- Convert Date Columns ---
    # Convert date columns to datetime objects
    date_columns = ["Date immatriculation", "Date radiation"]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # --- Trim Whitespace for Text Columns ---
    # For all columns with object (string) data, strip leading and trailing spaces
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].str.strip()

    # --- (Optional) Additional Cleaning ---
    # For instance, if you want to fill missing 'Nom commercial' values with a default value:
    # df['Nom commercial'] = df['Nom commercial'].fillna("Non spécifié")

    # Save the cleaned DataFrame to a new CSV file using the semicolon as a delimiter
    df.to_csv(output_file, sep=";", index=False)
    print(f"Cleaned data saved to {output_file}")


if __name__ == "__main__":
    # Define the input and output file paths
    input_file = "./ETL/data/output/extract/entreprises_radiees.csv"
    output_file = "./ETL/data/output/transform/entreprises_radiees.csv"

    # Run the cleaning process
    clean_entreprises_radiees(input_file, output_file)

import pandas as pd


def clean_chiffres_cles(input_file: str, output_file: str):
    # Load the CSV file
    df = pd.read_csv(input_file, sep=";")

    # Replace the string "Confidentiel" with NaN throughout the DataFrame
    df.replace("Confidentiel", pd.NA, inplace=True)

    # --- Clean Identifier Columns ---
    # Convert 'Siren' to string and trim whitespace
    if "Siren" in df.columns:
        df["Siren"] = df["Siren"].astype(str).str.strip()

    # Convert 'Nic' to string and remove any trailing decimal (e.g., "20.0" -> "20")
    if "Nic" in df.columns:
        df["Nic"] = df["Nic"].astype(str).str.split(".").str[0]

    # --- Clean Postal and Department Codes ---
    # Convert 'Code postal' to string and remove trailing '.0'
    if "Code postal" in df.columns:
        df["Code postal"] = (
            df["Code postal"]
            .astype(str)
            .str.replace(r"\.0$", "", regex=True)
            .str.strip()
        )

    # Convert 'Num. dept.' to string and remove trailing '.0'
    if "Num. dept." in df.columns:
        df["Num. dept."] = (
            df["Num. dept."]
            .astype(str)
            .str.replace(r"\.0$", "", regex=True)
            .str.strip()
        )

    # --- Convert Date Columns ---
    # Identify columns containing "Date" and convert them to datetime (day-first format)
    date_columns = [col for col in df.columns if "Date" in col]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

    # --- Convert Financial Columns ---
    # Identify columns containing "CA " or "Résultat" and convert them to numeric
    financial_columns = [col for col in df.columns if "CA " in col or "Résultat" in col]
    for col in financial_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # --- (Optional) Remove duplicates based on 'Siren' ---
    df.drop_duplicates(subset=["Siren"], inplace=True)

    # Save the cleaned DataFrame to a new CSV file
    df.to_csv(output_file, sep=";", index=False)
    print(f"Cleaned data saved to {output_file}")


if __name__ == "__main__":
    # Define input and output files
    input_file = "./ETL/data/output/extract/chiffres_cles.csv"
    output_file = "./ETL/data/output/transform/chiffres_cles.csv"

    # Run the cleaning process
    clean_chiffres_cles(input_file, output_file)

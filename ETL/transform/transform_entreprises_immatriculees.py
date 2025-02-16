import pandas as pd
import numpy as np


def clean_entreprises_immatriculees(input_file: str, output_file: str):
    # Lire le fichier CSV avec ";" comme séparateur
    df = pd.read_csv(input_file, sep=";")

    # Remplacer les chaînes vides par NaN pour plus de cohérence
    df.replace(r"^\s*$", np.nan, regex=True, inplace=True)

    # --- Nettoyer les colonnes d'identifiants ---
    # Convertir 'Siren' en chaîne de caractères et supprimer les espaces
    if "Siren" in df.columns:
        df["Siren"] = df["Siren"].astype(str).str.strip()

    # Convertir 'Nic' en chaîne de caractères, supprimer la décimale éventuelle (ex: "13.0" -> "13")
    if "Nic" in df.columns:
        df["Nic"] = df["Nic"].astype(str).str.split(".").str[0].str.strip()

    # --- Nettoyer les codes postaux ---
    # Convertir 'Code postal' en chaîne de caractères, supprimer les espaces,
    # remplacer le point isolé par une chaîne vide, et enlever les éventuels ".0" en fin de chaîne.
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

    # --- Convertir les colonnes de dates ---
    # Convertir les colonnes de dates en datetime
    date_columns = ["Date immatriculation", "Date radiation"]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # --- Supprimer les espaces en trop pour les colonnes textuelles ---
    text_cols = df.select_dtypes(include=["object"]).columns
    for col in text_cols:
        df[col] = df[col].str.strip()

    # Sauvegarder le DataFrame nettoyé dans un nouveau fichier CSV
    df.to_csv(output_file, sep=";", index=False)
    print(f"Cleaned data saved to {output_file}")


if __name__ == "__main__":
    # Définir les chemins d'entrée et de sortie
    input_file = "./ETL/data/output/extract/entreprises_immatriculees.csv"
    output_file = "./ETL/data/output/transform/entreprises_immatriculees.csv"

    # Exécuter le processus de nettoyage
    clean_entreprises_immatriculees(input_file, output_file)

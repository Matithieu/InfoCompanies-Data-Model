import pandas as pd


# Function to check and clean 'Siren' column
def clean_siren_column(dataframe):
    # Ensure all values in the 'Siren' column are strings
    dataframe["Siren"] = dataframe["Siren"].astype(str)
    # Remove non-digit characters
    dataframe["Siren"] = dataframe["Siren"].str.replace(r"\D", "", regex=True)
    # Convert to integer, coercing errors to NaN
    dataframe["Siren"] = pd.to_numeric(dataframe["Siren"], errors="coerce").astype(
        "Int64"
    )
    return dataframe


# Liste des chemins des fichiers à concaténer
chemins_des_fichiers = [
    "./fichier_chiffres.csv",
    "./fichier_immatriculees.csv",
    "./fichier_radiees.csv",
]

# Créez un DataFrame vide pour stocker les données combinées
data_combine = pd.DataFrame()

# Bouclez à travers les fichiers et chargez-les dans des DataFrames
for chemin in chemins_des_fichiers:
    print(f"Chargement du fichier {chemin}...")
    data = pd.read_csv(chemin, sep=";", low_memory=False)

    # Check and clean 'Siren' column
    data = clean_siren_column(data)

    # Debugging: print problematic lines if any
    if data["Siren"].isnull().any():
        print(f"Des valeurs non valides dans le fichier {chemin} :")
        print(data[data["Siren"].isnull()])

    # Fusionnez les données avec le DataFrame combiné
    data_combine = pd.concat([data_combine, data], ignore_index=True, sort=False)

# Supprimez les doublons en utilisant la colonne "Siren"
data_combine = data_combine.drop_duplicates(subset=["Siren"])

# Enregistrez le DataFrame combiné dans un nouveau fichier CSV
data_combine.to_csv("fichier_combine.csv", sep=";", index=False)
print("Fichier final enregistré avec succès !")

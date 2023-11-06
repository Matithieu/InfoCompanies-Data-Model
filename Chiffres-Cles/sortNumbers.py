import pandas as pd
import glob

# Define the path pattern for CSV files
modele_nom_fichier = "./Chiffres-Cles/chiffres-cles-*.csv"
chemins_des_fichiers = glob.glob(modele_nom_fichier)

# Specify the columns to keep
colonnes_a_conserver = [
    "Dénomination",
    "Siren",
    "Nic",
    "Forme Juridique",
    "Code APE",
    "Adresse",
    "Code postal",
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

data_frames = {}

# Load each CSV file and store in a dictionary with year as key
for chemin in chemins_des_fichiers:
    print(f"Chargement du fichier {chemin}...")
    data = pd.read_csv(chemin, sep=";", usecols=colonnes_a_conserver)
    data["Siren"] = data["Siren"].astype(str)
    year = chemin.split("-")[-1].split(".")[0]

    # Rename only financial columns for each year
    financial_columns = [col for col in data.columns if col.startswith(("Date de cloture ", "CA ", "Résultat "))]

    # For clarity, you might not want to rename the first year's columns
    if year != "2018":  # assuming 2018 is your first year; adjust as needed
        data.rename(columns={col: f"{col} - {year}" for col in financial_columns}, inplace=True)

    data_frames[year] = data

# Initialize an empty DataFrame for combined data
combined_data = pd.DataFrame()

# Merge data from different years
for annee, data_annee in data_frames.items():
    if combined_data.empty:
        combined_data = data_annee
    else:
        combined_data = pd.merge(combined_data, data_annee, on="Siren", how="left", suffixes=('', '_y'))

# Remove any duplicate columns (those ending with '_y')
combined_data = combined_data.loc[:, ~combined_data.columns.str.endswith('_y')]

# Drop duplicates based on 'Siren'
combined_data = combined_data.drop_duplicates(subset=["Siren"])

# Save the combined DataFrame to a new CSV file
nouveau_nom_fichier = "fichier_chiffres.csv"
combined_data.to_csv(nouveau_nom_fichier, index=False, sep=";")
print(f'Le fichier CSV combiné, trié et sans doublons a été enregistré sous "{nouveau_nom_fichier}".')

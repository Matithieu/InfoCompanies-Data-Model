import pandas as pd

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
    data = pd.read_csv(chemin, sep=";")

    # Fusionnez les données avec le DataFrame combiné
    data_combine = pd.concat([data_combine, data], ignore_index=True, sort=False)

# Supprimez les doublons en utilisant la colonne "Siren" (ou une autre colonne appropriée)
data_combine = data_combine.drop_duplicates(subset=["Siren"])

data_sorted = data_combine.sort_values(by=["Code APE"])

# Enregistrez le DataFrame combiné dans un nouveau fichier CSV
data_sorted.to_csv("fichier_combine.csv", sep=";", index=False)
print("Fichier final enregistré avec succès !")

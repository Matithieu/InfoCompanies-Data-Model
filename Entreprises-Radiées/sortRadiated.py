import pandas as pd
import glob

# Modèle de nom de fichier avec un wildcard (*) pour correspondre à toutes les années
modele_nom_fichier = "./Entreprises-Radiées/societes-radiees-*.csv"

# Liste tous les fichiers correspondant au modèle de nom de fichier
chemins_des_fichiers = glob.glob(modele_nom_fichier)

# Définissez les colonnes que vous souhaitez conserver
colonnes_a_conserver = [
    "Dénomination",
    "Siren",
    "Nic",
    "Forme Juridique",
    "Code APE",
    "Secteur d'activité",
    "Adresse",
    "Code postal",
    "Ville",
    "Région",
    "Date immatriculation",
    "Date radiation",
]

# Créez une liste vide pour stocker les DataFrames individuels
frames = []

# Bouclez à travers les fichiers et chargez-les dans des DataFrames
for chemin in chemins_des_fichiers:
    print(f"Chargement du fichier {chemin}...")
    data = pd.read_csv(chemin, sep=";", usecols=colonnes_a_conserver)
    frames.append(data)

# Concaténez tous les DataFrames en un seul DataFrame
data_combine = pd.concat(frames, ignore_index=True)

# Enregistrez le DataFrame combiné dans un nouveau fichier CSV
data_combine.to_csv("fichier_radiees.csv", sep=';', index=False)
print("Fichier final enregistré avec succès !")

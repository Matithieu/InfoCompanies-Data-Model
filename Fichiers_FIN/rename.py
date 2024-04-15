import pandas as pd

# Spécifiez le chemin vers votre fichier CSV existant
chemin_fichier_exist = './fichier_combine.csv'

# Les nouvelles colonnes que vous souhaitez ajouter comme en-têtes
nouvelles_colonnes = [
    'phone', 'website', 'reviews', 'schedule',
    'instagram', 'facebook', 'twitter', 'linkedin', 'youtube', 'email',
    'dateOfScrapping'
]

# Lire le fichier CSV existant avec pandas
donnees_existantes = pd.read_csv(chemin_fichier_exist, sep=';')

# Ajouter les nouvelles colonnes
donnees_existantes = pd.concat([donnees_existantes, pd.DataFrame(columns=nouvelles_colonnes)])

# Enregistrez le DataFrame mis à jour dans le même fichier CSV
donnees_existantes.to_csv(chemin_fichier_exist, sep=';', index=False)

print(f"Les en-têtes ont été ajoutés avec succès au fichier : {chemin_fichier_exist}")
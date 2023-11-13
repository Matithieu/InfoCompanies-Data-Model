import pandas as pd

colonnes_a_conserver = [
    "Siren",
    "Phone",
    "Website",
    "Reviews",
    "Schedule",
    "Instagram",
    "Facebook",
    "Twitter",
    "LinkedIn",
    "Youtube",
    "Email",
    "DateOfScraping"    
]

# Lecture des fichiers CSV
df1 = pd.read_csv('./fichier_combine.csv', delimiter=';')
df2 = pd.read_csv('./fichier_combine_updated.csv', delimiter=';', usecols=colonnes_a_conserver)

# Fusion des dataframes
print("Combining...")
df_merged = pd.merge(df1, df2, on='Siren', how='left')

# Nettoyage post-fusion (si nécessaire)
print("Cleaning...")
df_merged = df_merged.drop_duplicates(subset=['Siren'])

# Sauvegarde du nouveau CSV
df_merged.to_csv('./csv_fusionne.csv', index=False, sep=';')
print("Merging done.")

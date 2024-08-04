import pandas as pd

# Chargement du fichier CSV
print("Loading Leaders CSV to rename")
df = pd.read_csv("leaders_sorted.csv", delimiter=";")

# Dictionnaire de traduction des en-têtes
translation_dict = {
    "Siren": "siren",
    "Qualité": "role",
    "Nom Patronymique": "last_name",
    "Prénoms": "first_name",
    "Numéro de Gestion": "gestion_number",
    "Type": "type",
    "Libellé Evènement": "event_name",
    "Greffe": "greffe",
    "date_greffe": "date_of_greffe",
    "Nom d'usage": "usage_name",
    "Pseudonyme": "pseudo",
    "Dénomination": "company_name",
    "Forme_Juridique": "legal_form",
    "id": "id_data",
}

# Renommer les en-têtes en utilisant le dictionnaire de traduction
print("Renaming Leaders CSV Columns")
df = df.rename(columns=translation_dict)

print("Leaders renaming done!")
# Enregistrement du fichier CSV avec les nouveaux en-têtes
df.to_csv("leaders_renamed.csv", index=False, sep=";")

# Dictionnaire de traduction des en-têtes
translation_dict = {
    "Siren": "siren",
    "Qualité": "role",
    "Nom Patronymique": "last_name",
    "Prénoms": "first_name",
    "Numéro de Gestion": "gestion_number",
    "Type": "type",
    "Libellé Evènement": "event_name",
    "Nom d'usage": "usage_name",
    "Pseudonyme": "pseudo",
    "Dénomination": "company_name",
    "Forme_Juridique": "legal_form",
    "id": "id_data",
}

# Chargement du fichier CSV
print("Loading Leaders CSV to rename")
with open("leaders_sorted.csv", "r", encoding="utf-8") as file:
    lines = file.readlines()

# Séparer la première ligne et les autres lignes
headers = lines[0].strip().split(";")
data = lines[1:]

# Renommer les en-têtes en utilisant le dictionnaire de traduction
print("Renaming Leaders CSV Columns")
new_headers = [translation_dict.get(header, header) for header in headers]

# Ecrire le fichier CSV avec les nouveaux en-têtes
print("Leaders renaming done!")
with open("leaders_renamed.csv", "w", encoding="utf-8") as file:
    file.write(";".join(new_headers) + "\n")
    file.writelines(data)

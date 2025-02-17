import os
import csv

# Dossier contenant les fichiers CSV
input_dir = "./ETL/data/input"
log_file = "./logs/encoding_issues.log"


def detect_encoding_issues(file_path):
    """
    Vérifie si un fichier CSV contient des problèmes d'encodage.
    Renvoie une liste des lignes problématiques.
    """
    issues = []

    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            print(f"Analyse de {file_path}...")
            reader = csv.reader(f, delimiter=";")  # Délimiteur spécifique
            for line_number, row in enumerate(reader, start=1):
                row_text = ";".join(row)  # Fusionner les colonnes pour analyse

                # Vérifier la présence de caractères mal encodés
                if "Ã" in row_text or "Â" in row_text or "�" in row_text:
                    issues.append(f"{file_path} | Ligne {line_number} : {row_text}")

    except Exception as e:
        issues.append(f"Erreur d'ouverture {file_path} : {str(e)}")

    return issues


# Récupérer tous les fichiers CSV de manière récursive
csv_files = []
for root, _, files in os.walk(input_dir):
    for file in files:
        if file.endswith(".csv"):
            csv_files.append(os.path.join(root, file))

# Vérifier chaque fichier et stocker les erreurs
all_issues = []

for csv_file in csv_files:
    issues = detect_encoding_issues(csv_file)
    all_issues.extend(issues)

# Sauvegarde des erreurs dans un fichier log
with open(log_file, "w", encoding="utf-8") as log:
    if all_issues:
        log.write("\n".join(all_issues))
        print(f"⚠️ Problèmes détectés ! Voir {log_file} pour les détails.")
    else:
        log.write("✅ Aucun problème d'encodage détecté.")
        print("✅ Aucun problème d'encodage détecté.")

# Affichage rapide des 5 premières erreurs (s'il y en a)
if all_issues:
    print("\n".join(all_issues[:5]))
    if len(all_issues) > 5:
        print(f"... {len(all_issues) - 5} autres erreurs trouvées.")

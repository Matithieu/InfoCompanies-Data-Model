import os

import chardet

# Dossier des fichiers CSV
input_dir = "./ETL/data/input"

# Récupération récursive des fichiers CSV
csv_files = []
for root, _, files in os.walk(input_dir):
    for file in files:
        if file.endswith(".csv"):
            csv_files.append(os.path.join(root, file))

# Vérification de l'encodage
encoding_issues = []

for csv_file in csv_files:
    with open(csv_file, "rb") as f:
        raw_data = f.read(100_000)  # Analyse des 100 000 premiers octets
        result = chardet.detect(raw_data)
        encoding = result["encoding"]
        confidence = result["confidence"]

    if encoding and confidence >= 0.75 and encoding.lower() != "utf-8":
        encoding_issues.append(
            f"{csv_file} | Encodage détecté : {encoding} (Confiance: {confidence:.2f})"
        )

# Affichage du rapport
if encoding_issues:
    print("⚠️ Encodages suspects détectés :")
    print("\n".join(encoding_issues))
    print("\n➡️ Solution : Convertir ces fichiers en UTF-8 pour éviter les erreurs.")
else:
    print("✅ Tous les fichiers sont en UTF-8 !")

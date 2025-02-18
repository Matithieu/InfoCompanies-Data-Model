import os
import codecs

# Répertoires
input_dir = "./ETL/data/input"
backup_dir = "./ETL/data/backup"

# Créer le dossier de backup s'il n'existe pas
os.makedirs(backup_dir, exist_ok=True)

# Trouver tous les fichiers CSV
for root, _, files in os.walk(input_dir):
    for file in files:
        if file.endswith(".csv"):
            file_path = os.path.join(root, file)

            # Lire le fichier avec UTF-8-SIG et réécrire en UTF-8 standard
            with codecs.open(file_path, "r", encoding="utf-8-sig") as f:
                content = f.read()

            # Sauvegarde de l'original
            backup_path = os.path.join(backup_dir, file)
            os.rename(file_path, backup_path)

            # Réécriture en UTF-8 standard
            with codecs.open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"✅ Fichier converti : {file}")

print("\n🚀 Conversion terminée ! Tous les fichiers sont désormais en UTF-8.")

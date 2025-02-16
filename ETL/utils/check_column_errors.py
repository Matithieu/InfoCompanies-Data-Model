import pandas as pd
import glob

# Chemin du dossier contenant les CSV
folder_path = "./ETL/data/output/transform/"

# Liste de tous les fichiers CSV dans le dossier
csv_files = glob.glob(folder_path + "*.csv")

column_to_check = "Code postal"
columns_to_display = ["Dénomination", column_to_check]

# Parcourir tous les fichiers CSV
for file in csv_files:
    print(f"📂 Traitement du fichier : {file}")

    try:
        # Charger le CSV
        df = pd.read_csv(file, sep=";", dtype=str)

        # Filtrer les lignes où le code postal contient un "."
        rows_with_dot = df[df[column_to_check].str.contains(r"\.", na=False)]

        # Afficher les résultats si des erreurs sont trouvées
        if not rows_with_dot.empty:
            print(rows_with_dot[columns_to_display])
        else:
            print("✅ Aucune erreur trouvée.\n")

    except Exception as e:
        print(f"❌ Erreur lors de la lecture de {file} : {e}\n")

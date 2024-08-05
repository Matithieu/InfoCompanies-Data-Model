import pandas as pd

path_of_file = "./Leaders/leaders.csv"

columns_to_keep = [
    "Siren",
    "Qualité",
    "Nom Patronymique",
    "Prénoms",
    "Numéro de Gestion",
    "Type",
    "Libellé Evènement",
    "Nom d'usage",
    "Pseudonyme",
    "Dénomination",
    "Forme_Juridique",
    "id",
]

print(f"Chargement du fichier {path_of_file} en chunks...")

chunk_size = 500_000  # Adjust the chunk size based on your memory capacity
chunks = []
for chunk in pd.read_csv(
    path_of_file,
    sep=";",
    usecols=columns_to_keep,
    chunksize=chunk_size,
):
    chunks.append(chunk)

data = pd.concat(chunks, ignore_index=True)
print("debug")

data.to_csv("leaders_sorted.csv", sep=";", index=False)
print("Sorted Leaders done !")

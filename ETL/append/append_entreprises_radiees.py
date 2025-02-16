import pandas as pd
import requests

# Charger le fichier CSV existant
df = pd.read_csv("./Entreprises-Radiées/societes-radiees-en-2023.csv", sep=";")

# Appeler l'API et obtenir les données (les 100 premiers résultats)
api_url = "https://opendata.datainfogreffe.fr/api/explore/v2.1/catalog/datasets/entreprises-radiees-en-2023/records?select=*&order_by=date_radiation%20DESC&limit=20"
response = requests.get(api_url)
data_api = response.json()

# Itérer sur les résultats et ajouter chaque résultat au DataFrame
for result in data_api["results"]:
    nouvelles_donnees = {
        "Dénomination": result["denomination"],
        "Siren": result["siren"],
        "Nic": result["nic"],
        "Forme Juridique": result["forme_juridique"],
        "Code APE": result["code_ape"],
        "Secteur d'activité": result["secteur_d_activite"],
        "Adresse": result["adresse"],
        "Code postal": result["code_postal"],
        "Ville": result["ville"],
        "Num. dept.": result["num_dept"],
        "Département": result["departement"],
        "Région": result["region"],
        "Code Greffe": result["code_greffe"],
        "Greffe": result["greffe"],
        "Date immatriculation": result["date_immatriculation"],
        "Date radiation": result["date_radiation"],
        "Statut": result["statut"],
        # t"Geolocalisation": f"({result['geolocalisation']['lon']}, {result['geolocalisation']['lat']})",
        "Date de publication": result["date_de_publication"],
        "Nom commercial": result["nom_commercial"],
        "Date immatriculation origine": result["date_immatriculation_origine"],
        "Sigle": result["sigle"],
        "Devise": result["devise"],
        "Durée": result["duree"],
        "Date cloture 1er exercice": result["date_cloture_1er_exercice"],
        "Date arreté des comptes": result["date_arrete_des_comptes"],
        "Etat": result["etat"],
        "etat_pub": result["etat_pub"],
        "fiche_identite": result["fiche_identite"],
    }
    # Ajouter les nouvelles données au DataFrame
    df = df._append(nouvelles_donnees, ignore_index=True)

# Enlever les doublons basés sur la colonne "Siren"
df = df.drop_duplicates(subset="Siren")

# Enregistrer le DataFrame mis à jour dans le fichier CSV
df.to_csv("fichier_radiees.csv", index=False, sep=";")
print("Fichier des entreprises radiées en CSV mis à jour avec succès !")

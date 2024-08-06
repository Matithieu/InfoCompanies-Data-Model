#!/bin/bash

# To compute all the data, you can run this script

# Then, to insert the data into the db, go to cd ..
# And run ./devcli insert_db

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Pas de couleur

# Liste des chemins vers vos scripts Python et le chemin vers le programme C
scripts=(
    "Chiffres-Cles/sortNumbers.py"
    "Entreprises-crées/addNewCompanies.py"
    "Entreprises-crées/sortCompanies.py"
    "Entreprises-Radiées/newRadiatedCompanies.py"
    "Entreprises-Radiées/sortRadiated.py"
    "Final-Sort/combined-data.py"
    "Final-Sort/Rename/add-columns.py"
    "Final-Sort/Rename/rename-columns.py"
    "Effectif/clean.py"
    "Effectif/merge-effectif.py"
    "Leaders/clean-leaders.py"
    "Leaders/rename-leaders.py"
)

# Liste des chemins vers les fichiers CSV à supprimer
csv_files_to_delete=(
    "city.csv"
    "fichier_chiffres.csv"
    #"fichier_combine_updated.csv"
    "fichier_combine.csv"
    "fichier_immatriculees.csv"
    "fichier_radiees.csv"
    "fichier_renamed.csv"
    "fichier_effectif.csv"
    "renamedColumns.csv"
    "industry_sector.csv"
    "leaders_renamed.csv"
    "leaders_sorted.csv"
    "legal_form.csv"
    "leaders_sorted.csv"
    #"merged_output.csv"
)

# Fonction pour supprimer les fichiers CSV
delete_csv_files() {
    for file in "${csv_files_to_delete[@]}"; do
        if [ -f "$file" ]; then
            rm -f "$file"
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}Le fichier $file a été supprimé avec succès !${NC}"
            else
                echo -e "${RED}Une erreur s'est produite lors de la suppression du fichier $file${NC}"
            fi
        else
            echo -e "${YELLOW}Le fichier $file n'existe pas.${NC}"
        fi
    done
}

# Capturer le temps de début
start_time=$(date +%s)

# Boucle pour exécuter chaque script
for script_path in "${scripts[@]}"; do
    if [[ $script_path == *.py ]]; then
        python3 "$script_path"
    else
        "$script_path"
    fi

    # Vérifie le statut de la dernière commande exécutée
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Le script $script_path a été exécuté avec succès !${NC}"
    else
        echo -e "${RED}Une erreur s'est produite lors de l'exécution du script $script_path${NC}"
    fi
done

echo "Tous les scripts ont été exécutés."

# Appel de la fonction pour supprimer les fichiers CSV
delete_csv_files

# Capturer le temps de fin
end_time=$(date +%s)

# Calculer le temps écoulé
elapsed_time=$((end_time - start_time))

minutes=$((elapsed_time / 60))
seconds=$((elapsed_time % 60))
echo -e "${YELLOW}Temps total écoulé : ${minutes}m ${seconds}s${NC}"

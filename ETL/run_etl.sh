#!/bin/bash
# ETL Runner Script
# This script runs your ETL pipeline by executing all extraction, transformation,
# and combination scripts in sequence. Once completed, it deletes intermediate CSV files.
#
# After processing, you can go up one directory and run:
# ./devcli insert_db

# Colors for output messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'  # No Color

# Updated list of ETL scripts (relative paths)
scripts=(
    "ETL/extract/extract_chiffres_cles.py"
    "ETL/extract/extract_effectif.py"
    "ETL/extract/extract_entreprises_immatriculees.py"
    "ETL/extract/extract_entreprises_radiees.py"
    # "ETL/extract/extract_leaders.py"
    #
    "ETL/transform/transform_chiffres_cles.py"
    "ETL/transform/transform_entreprises_immatriculees.py"
    "ETL/transform/transform_entreprises_radiees.py"
    # "ETL/transform/transform_leaders.py"
    #
    "ETL/combine/combine_fichier_combine.py"
    "ETL/combine/transform_fichier_combine.py"
    "ETL/combine/combine_effectif_to_fichier_combine.py"
    #
    "ETL/transform/transform_final.py"
)

# List of intermediate CSV files to delete (update as needed)
csv_files_to_delete=(
    "./ETL/data/output/extract/chiffres_cles.csv"
    "./ETL/data/output/extract/entreprises_immatriculees.csv"
    "./ETL/data/output/extract/entreprises_radiees.csv"
    "./ETL/data/output/extract/leaders.csv"
    "./ETL/data/output/extract/stock_unite_legale.csv"
    #
    "./ETL/data/output/transform/chiffres_cles.csv"
    "./ETL/data/output/transform/entreprises_immatriculees.csv"
    "./ETL/data/output/transform/entreprises_radiees.csv"
    # "./ETL/data/output/transform/leaders.csv"
    "./ETL/data/output/transform/fichier_combine.csv"
    #
    "./ETL/data/output/combine/fichier_combine.csv"
    "./ETL/data/output/combine/fichier_effectif_and_combine.csv"
    "./ETL/data/output/effectif/fichier_effectif.csv"
)

# Function to run ETL scripts
run_scripts() {
    echo -e "${YELLOW}Running ETL scripts...${NC}"
    for script in "${scripts[@]}"; do
        if [[ "$script" == *.py ]]; then
            if [ -f "$script" ]; then
                echo -e "${YELLOW}Executing: $script${NC}"
                start_time=$(date +%s)
                python3 "$script"
                end_time=$(date +%s)
            else
                echo -e "${RED}Script not found: $script${NC}"
                continue
            fi
        else
            if [ -x "$script" ]; then
                start_time=$(date +%s)
                "$script"
                end_time=$(date +%s)
            else
                echo -e "${RED}File not executable or not found: $script${NC}"
                continue
            fi
        fi
        
        # Check the exit status of the script
        if [ $? -eq 0 ]; then
            elapsed=$((end_time - start_time))
            echo -e "${GREEN}Executed successfully: $script in ${elapsed}s${NC}"
        else
            echo -e "${RED}Error executing: $script${NC}"
        fi
    done
}

# Function to delete intermediate CSV files
delete_csv_files() {
    echo -e "${YELLOW}Deleting intermediate CSV files...${NC}"
    for file in "${csv_files_to_delete[@]}"; do
        if [ -f "$file" ]; then
            rm -f "$file"
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}Deleted: $file${NC}"
            else
                echo -e "${RED}Error deleting: $file${NC}"
            fi
        else
            echo -e "${YELLOW}File not found: $file${NC}"
        fi
    done
}

# Main execution block
main() {
    echo -e "${YELLOW}Starting ETL process...${NC}"
    main_start_time=$(date +%s)
    
    run_scripts
    echo -e "${GREEN}All ETL scripts executed.${NC}"
    
    delete_csv_files
    
    main_end_time=$(date +%s)
    elapsed=$((main_end_time - main_start_time))
    minutes=$((elapsed / 60))
    seconds=$((elapsed % 60))
    echo -e "${YELLOW}Total elapsed time: ${minutes}m ${seconds}s${NC}"
    echo -e "${GREEN}ETL process completed.${NC}"
}

main
#!/bin/bash

# To launch the script: sudo -E ./db.sh
# On zsh: sudo -E sh db.sh

# python3 ./startScripts.py

# chmod +r ./fichier_combine.csv
# cp ./fichier_combine.csv /tmp/fichier_combine.csv

# python3 Fichiers_FIN/renameColumnsFinal.py
CSV_FILE="$1"
sudo chmod +r "./InfoCompanies-Data-Model/$CSV_FILE"
sudo cp "./InfoCompanies-Data-Model/$CSV_FILE" "/tmp/$CSV_FILE"
# sudo -E python3 ./clean.py

csv_file="/tmp/$CSV_FILE"
container_csv_file="/csv/$CSV_FILE"

# Verify if the CSV file exists
if [ ! -f "$csv_file" ]; then
    echo "The CSV file '$csv_file' doesn't exist."
    exit 1
fi

# Function to get the PostgreSQL container ID
get_postgres_container_id() {
    docker ps --filter "ancestor=postgres" --format "{{.ID}}"
}

# Function to transfer the CSV file to the PostgreSQL database
transfer_csv_to_database() {
    local postgres_container
    postgres_container=$(get_postgres_container_id)
    if [ -z "$postgres_container" ]; then
        echo "No running PostgreSQL container found."
        exit 1
    fi

    # Create indexes
    docker exec -u postgres -it "$postgres_container" psql -d postgres -c "CREATE INDEX IF NOT EXISTS idx_siren_number ON companies (siren_number);"
    docker exec -u postgres -it "$postgres_container" psql -d postgres -c "CREATE INDEX IF NOT EXISTS idx_company_name ON companies (company_name);"

    local columns
    columns=$(head -1 "$csv_file" | tr ';' ',')

    # Transfer the CSV file to the PostgreSQL database and create the indexes
    docker exec -u postgres -it "$postgres_container" psql -d postgres -c "\copy companies($columns) FROM '$container_csv_file' DELIMITER ';' CSV HEADER;"
}

# Function to remove the error line from the CSV file
remove_error_line() {
    # Delete the line from the CSV file
    sed -i "$1d" "$csv_file"
}

# Backup the CSV file
cp "$csv_file" "$csv_file.bak"

# Transfer the CSV file to the PostgreSQL database
output=$(transfer_csv_to_database 2>&1)

# Verify if the transfer was successful
if [ $? -ne 0 ]; then
    # Extract the line number from the error message
    line_number=$(echo "$output" | grep -oE 'LINE [0-9]+' | grep -oE '[0-9]+')

    if [ -n "$line_number" ]; then
        echo "Error at the line $line_number. Deleting the line."

        # Remove the error line from the CSV file
        remove_error_line "$line_number"

        # Retry the transfer
        transfer_csv_to_database
    else
        echo "Error during the transfer of the CSV file to the PostgreSQL database : $output"
        # Restore the backup
        mv "$csv_file.bak" "$csv_file"
    fi
else
    echo "Transfer of the CSV file to the PostgreSQL database successful."
fi

python3 ./InfoCompanies-Data-Model/Fichiers_FIN/insert.py

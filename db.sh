#!/bin/bash

csv_file='/tmp/final.csv'

# Verify if the CSV file exists
if [ ! -f "$csv_file" ]; then
    echo "The CSV file '$csv_file' doen't exist. Don't forget to do chmod +x"
    exit 1
fi

# Function to transfer the CSV file to the PostgreSQL database
transfer_csv_to_database() {
    local columns=$(head -1 "$csv_file" | tr ';' ',')
    # Transférer le fichier CSV dans la base de données PostgreSQL
    sudo -u postgres psql -d postgres -c "\copy companies($columns) FROM '$csv_file' DELIMITER ';' CSV HEADER;"
}

# Fuction to remove the error line from the CSV file
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

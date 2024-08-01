#!/bin/bash

# To launch the script: sudo -E ./db.sh
# On zsh: sudo -E sh db.sh

CSV_FILE="$1"
ACTION="$2"

# Function to get the PostgreSQL container ID
get_postgres_container_id() {
    docker ps --filter "ancestor=postgres" --format "{{.ID}}"
}

# Function to transfer the CSV file to the PostgreSQL database
transfer_csv_to_database() {
    local csv_file="/tmp/$CSV_FILE"
    local container_csv_file="/csv/$CSV_FILE"

    # Verify if the CSV file exists
    if [ ! -f "$csv_file" ]; then
        echo "The CSV file '$csv_file' doesn't exist."
        exit 1
    fi

    local postgres_container
    postgres_container=$(get_postgres_container_id)
    if [ -z "$postgres_container" ]; then
        echo "No running PostgreSQL container found."
        exit 1
    fi

    local columns
    columns=$(head -1 "$csv_file" | tr ';' ',')

    # Transfer the CSV file to the PostgreSQL database
    docker exec -u postgres -it "$postgres_container" psql -d postgres -c "\copy companies($columns) FROM '$container_csv_file' DELIMITER ';' CSV HEADER;"
}

# Function to transfer the city CSV file to the PostgreSQL database
transfer_city_csv_to_database() {
    local city_csv_file="$1"
    local container_city_csv_file
    container_city_csv_file="/csv/$(basename "$city_csv_file")"
    sudo chmod +r "$city_csv_file"
    sudo cp "$city_csv_file" "/tmp/$(basename "$city_csv_file")"

    if [ ! -f "/tmp/$(basename "$city_csv_file")" ]; then
        echo "The city CSV file '/tmp/$(basename "$city_csv_file")' doesn't exist."
        exit 1
    fi

    local postgres_container
    postgres_container=$(get_postgres_container_id)
    if [ -z "$postgres_container" ]; then
        echo "No running PostgreSQL container found."
        exit 1
    fi

    local columns
    columns=name

    echo "Transferring the city CSV file to the PostgreSQL database."
    # Transfer the city CSV file to the PostgreSQL database
    docker exec -u postgres -it "$postgres_container" psql -d postgres -c "\copy city($columns) FROM '$container_city_csv_file' DELIMITER ',' CSV HEADER;"
}

# Function to create indexes in the PostgreSQL database
create_indexes() {
    local postgres_container
    postgres_container=$(get_postgres_container_id)
    if [ -z "$postgres_container" ]; then
        echo "No running PostgreSQL container found."
        exit 1
    fi

    docker exec -u postgres -it "$postgres_container" psql -d postgres -c "CREATE INDEX IF NOT EXISTS idx_siren_number ON companies (siren_number);"
    docker exec -u postgres -it "$postgres_container" psql -d postgres -c "CREATE INDEX IF NOT EXISTS idx_company_name ON companies (company_name);"
    docker exec -u postgres -it "$postgres_container" psql -d postgres -c "CREATE INDEX IF NOT EXISTS idx_company_seen_user_id ON company_seen (user_id);"
    docker exec -u postgres -it "$postgres_container" psql -d postgres -c "CREATE INDEX IF NOT EXISTS idx_company_seen_company_ids_company_ids ON company_seen_company_ids (company_ids);"
    docker exec -u postgres -it "$postgres_container" psql -d postgres -c "CREATE INDEX IF NOT EXISTS idx_company_seen_company_ids_company_seen_id ON company_seen_company_ids (company_seen_id);"
}

# Function to create indexes for the city, industry_sector, region, and legal_form tables in the PostgreSQL database
create_additional_indexes() {
    local postgres_container
    postgres_container=$(get_postgres_container_id)
    if [ -z "$postgres_container" ]; then
        echo "No running PostgreSQL container found."
        exit 1
    fi

    docker exec -u postgres -it "$postgres_container" psql -d postgres -c "CREATE INDEX IF NOT EXISTS idx_city_name ON city (name);"
    docker exec -u postgres -it "$postgres_container" psql -d postgres -c "CREATE INDEX IF NOT EXISTS idx_industry_sector_name ON industry_sector (name);"
    docker exec -u postgres -it "$postgres_container" psql -d postgres -c "CREATE INDEX IF NOT EXISTS idx_region_name ON region (name);"
    docker exec -u postgres -it "$postgres_container" psql -d postgres -c "CREATE INDEX IF NOT EXISTS idx_legal_form_name ON legal_form (name);"
}

# Function to remove the error line from the CSV file
remove_error_line() {
    local line_number="$1"
    local csv_file="/tmp/$CSV_FILE"
    # Delete the line from the CSV file
    sed -i "${line_number}d" "$csv_file"
}

# Main execution
case "$ACTION" in
transfer_city_csv_to_database)
    transfer_city_csv_to_database "/home/mathieu/InfoCompanies/InfoCompanies-Data-Model/city.csv"
    create_additional_indexes
    ;;
*)
    python3 ./startScripts.py

    sudo chmod +r "./InfoCompanies-Data-Model/$CSV_FILE"
    sudo cp "./InfoCompanies-Data-Model/$CSV_FILE" "/tmp/$CSV_FILE"

    # Backup the CSV file
    cp "/tmp/$CSV_FILE" "/tmp/$CSV_FILE.bak"

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
            output=$(transfer_csv_to_database 2>&1)

            if [ $? -ne 0 ]; then
                echo "Error during the transfer of the CSV file to the PostgreSQL database : $output"
                # Restore the backup
                mv "/tmp/$CSV_FILE.bak" "/tmp/$CSV_FILE"
                exit 1
            fi
        else
            echo "Error during the transfer of the CSV file to the PostgreSQL database : $output"
            # Restore the backup
            mv "/tmp/$CSV_FILE.bak" "/tmp/$CSV_FILE"
            exit 1
        fi
    fi

    echo "Transfer of the CSV file to the PostgreSQL database successful."

    # Create indexes
    create_indexes
    create_additional_indexes

    # Transfer the city CSV file to the PostgreSQL database
    transfer_city_csv_to_database "/home/mathieu/InfoCompanies/InfoCompanies-Data-Model/city.csv"

    # Create indexes for the city table
    create_additional_indexes

    # Check if the CSV file is the template
    if [ "$CSV_FILE" = "template.csv" ]; then
        echo "Skipping insertion as the CSV file is the template."
    else
        python3 ./InfoCompanies-Data-Model/Fichiers_FIN/insert.py
    fi
    ;;
esac

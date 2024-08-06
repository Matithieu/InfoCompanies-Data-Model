#!/bin/bash

# To launch the script: sudo -E ./db.sh
# On zsh: sudo -E sh db.sh

CSV_FILE="$1"
ACTION="$2"

# Function to get the PostgreSQL container ID
get_postgres_container_id() {
    docker ps --filter "ancestor=postgres" --format "{{.ID}}"
}

# Generic function to transfer a CSV file to the PostgreSQL database
transfer_csv_to_database() {
    local table_name="$1"
    local csv_file_path="$2"
    local columns="$3"
    local delimiter="$4"
    local base_name
    base_name=$(basename "$csv_file_path")
    local container_csv_file="/tmp/$base_name"

    # Verify if the CSV file exists
    if [ ! -f "$csv_file_path" ]; then
        echo "The CSV file '$csv_file_path' doesn't exist."
        exit 1
    fi

    sudo chmod +r "$csv_file_path"

    local postgres_container
    postgres_container=$(get_postgres_container_id)
    if [ -z "$postgres_container" ]; then
        echo "No running PostgreSQL container found."
        exit 1
    fi

    echo "Transferring the CSV file to the PostgreSQL database."
    docker cp "$csv_file_path" "$postgres_container:$container_csv_file"
    docker exec -u postgres -it "$postgres_container" psql -d postgres -c "\copy $table_name($columns) FROM '$container_csv_file' DELIMITER '$delimiter' CSV HEADER;"
}

# Function to create indexes for a given table and columns
create_indexes() {
    local table_name="$1"
    shift
    local columns=("$@")

    local postgres_container
    postgres_container=$(get_postgres_container_id)
    if [ -z "$postgres_container" ]; then
        echo "No running PostgreSQL container found."
        exit 1
    fi

    for column in "${columns[@]}"; do
        echo "Creating index idx_${table_name}_${column} on $table_name ($column)."
        docker exec -u postgres -it "$postgres_container" psql -d postgres -c "CREATE INDEX IF NOT EXISTS idx_${table_name}_${column} ON $table_name ($column);"
    done
}

# Function to remove the error line from the CSV file
remove_error_line() {
    local line_number="$1"
    local csv_file="$2"
    sed -i "${line_number}d" "$csv_file"
}

# Function to export unique values to a CSV file
export_unique_values() {
    local query="$1"
    local base_name
    base_name=$(basename "$2")
    local output_csv="/tmp/$base_name"

    local postgres_container
    postgres_container=$(get_postgres_container_id)
    if [ -z "$postgres_container" ]; then
        echo "No running PostgreSQL container found."
        exit 1
    fi

    # Ensure the /tmp directory exists and has the correct permissions
    docker exec -u postgres -it "$postgres_container" mkdir -p /tmp

    # Execute the query and export the results to the CSV file
    docker exec -u postgres -it "$postgres_container" psql -d postgres -c "\copy ($query) TO '$output_csv' CSV HEADER;"

    # Ensure the destination directory on the host machine has the correct permissions
    sudo chmod 777 "./InfoCompanies-Data-Model"

    # Copy the CSV file from the container to the host machine
    docker cp "$postgres_container:$output_csv" "./InfoCompanies-Data-Model/$(basename "$2")"
}

# Export all unique values at the start of the script
export_all_unique_values() {
    export_unique_values "SELECT DISTINCT industry_sector FROM public.companies" "./InfoCompanies-Data-Model/industry_sector.csv"
    export_unique_values "SELECT DISTINCT city FROM public.companies" "./InfoCompanies-Data-Model/city.csv"
    export_unique_values "SELECT DISTINCT legal_form FROM public.companies" "./InfoCompanies-Data-Model/legal_form.csv"
}

# Function to split and transfer CSV files in chunks
split_and_transfer_csv() {
    local table_name="$1"
    local csv_file_path="$2"
    local columns="$3"
    local delimiter="$4"
    local chunk_size="$5"

    split -l "$chunk_size" "$csv_file_path" chunk_

    for chunk in chunk_*; do
        transfer_csv_to_database "$table_name" "$chunk" "$columns" "$delimiter"
        rm "$chunk"
    done
}

# Main script
case "$ACTION" in
transfer_leaders_csv_to_database)
    split_and_transfer_csv "leader" "./InfoCompanies-Data-Model/leaders_renamed.csv" "$(head -1 "./InfoCompanies-Data-Model/leaders_renamed.csv" | tr ';' ',')" ";" 1000000
    ;;
transfer_city_csv_to_database)
    transfer_csv_to_database "city" "./InfoCompanies-Data-Model/city.csv" "name" ","
    ;;
transfer_industry_sector_csv_to_database)
    transfer_csv_to_database "industry_sector" "./InfoCompanies-Data-Model/industry_sector.csv" "name" ","
    ;;
export_unique_industry_sector)
    export_unique_values "SELECT DISTINCT industry_sector FROM public.companies" "./InfoCompanies-Data-Model/industry_sector.csv"
    ;;
export_unique_cities)
    export_unique_values "SELECT DISTINCT city FROM public.companies" "./InfoCompanies-Data-Model/city.csv"
    ;;
export_unique_values)
    query="$3"
    output_csv="$4"
    export_unique_values "$query" "$output_csv"
    ;;
*)
    sudo chmod +r "./InfoCompanies-Data-Model/$CSV_FILE"

    # Backup the CSV file
    cp "./InfoCompanies-Data-Model/$CSV_FILE" "./InfoCompanies-Data-Model/$CSV_FILE.bak"

    # Transfer the CSV file to the PostgreSQL database
    output=$(transfer_csv_to_database "companies" "./InfoCompanies-Data-Model/$CSV_FILE" "$(head -1 "./InfoCompanies-Data-Model/$CSV_FILE" | tr ';' ',')" ";" 2>&1)

    # Verify if the transfer was successful
    if [ $? -ne 0 ]; then
        # Extract the line number from the error message
        line_number=$(echo "$output" | grep -oE 'LINE [0-9]+' | grep -oE '[0-9]+')

        if [ -n "$line_number" ]; then
            echo "Error at line $line_number. Deleting the line."

            # Remove the error line from the CSV file
            remove_error_line "$line_number" "./InfoCompanies-Data-Model/$CSV_FILE"

            # Retry the transfer
            output=$(transfer_csv_to_database "companies" "./InfoCompanies-Data-Model/$CSV_FILE" "$(head -1 "./InfoCompanies-Data-Model/$CSV_FILE" | tr ';' ',')" ";" 2>&1)

            if [ $? -ne 0 ]; then
                echo "Error during the transfer of the CSV file to the PostgreSQL database: $output"
                # Restore the backup
                mv "./InfoCompanies-Data-Model/$CSV_FILE.bak" "./InfoCompanies-Data-Model/$CSV_FILE"
                exit 1
            fi
        else
            echo "Error during the transfer of the CSV file to the PostgreSQL database: $output"
            # Restore the backup
            mv "./InfoCompanies-Data-Model/$CSV_FILE.bak" "./InfoCompanies-Data-Model/$CSV_FILE"
            exit 1
        fi
    fi

    echo "Transfer of the CSV file to the PostgreSQL database successful."

    # Main execution
    export_all_unique_values

    # Create indexes
    create_indexes "companies" "siren_number" "company_name" "legal_form" "industry_sector" "region" "city" "phone_number"
    create_indexes "company_seen" "user_id"
    create_indexes "company_seen_company_ids" "company_ids" "company_seen_id"
    create_indexes "city" "name"
    create_indexes "industry_sector" "name"
    create_indexes "legal_form" "name"
    create_indexes "leader" "siren" "company_name" "first_name" "last_name"

    transfer_csv_to_database "city" "./InfoCompanies-Data-Model/city.csv" "name" ","
    transfer_csv_to_database "industry_sector" "./InfoCompanies-Data-Model/industry_sector.csv" "name" ","
    transfer_csv_to_database "legal_form" "./InfoCompanies-Data-Model/legal_form.csv" "name" ","

    split_and_transfer_csv "leader" "./InfoCompanies-Data-Model/leaders_renamed.csv" "$(head -1 "./InfoCompanies-Data-Model/leaders_renamed.csv" | tr ';' ',')" ";" 1000000

    # Check if the CSV file is the template
    if [ "$CSV_FILE" = "template.csv" ]; then
        echo "Skipping insertion as the CSV file is the template."
    else
        python3 InfoCompanies-Data-Model/Final-Sort/Insert-DB/insert.py
        echo "Insertion of the data into the database successful."
    fi
    ;;
esac

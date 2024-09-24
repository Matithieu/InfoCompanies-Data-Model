#!/bin/bash

# To launch the script: sudo -E ./db.sh
# On zsh: sudo -E sh db.sh

CSV_FILE="$1"
ACTION="$2"

# Function to get the PostgreSQL container ID
get_postgres_container_id() {
    docker ps --filter "ancestor=postgres" --format "{{.ID}}"
}

# Function to enable the pg_trgm extension
enable_pg_trgm_extension() {
    local postgres_container
    postgres_container=$(get_postgres_container_id)
    if [ -z "$postgres_container" ]; then
        echo "No running PostgreSQL container found."
        exit 1
    fi

    echo "Enabling pg_trgm extension in the PostgreSQL database."
    docker exec -u postgres -it "$postgres_container" psql -d postgres -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"
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

# Function to create trigram indexes for text columns
create_trigram_indexes() {
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
        echo "Creating trigram index idx_${table_name}_${column}_trgm on $table_name ($column)."
        docker exec -u postgres -it "$postgres_container" psql -d postgres -c "CREATE INDEX IF NOT EXISTS idx_${table_name}_${column}_trgm ON $table_name USING gin (LOWER($column) gin_trgm_ops);"
    done
}

# Function to create composite indexes for a given table and set of columns
create_composite_index() {
    local table_name="$1"
    shift
    local columns=("$@")

    if [ ${#columns[@]} -lt 2 ]; then
        echo "At least two columns are required to create a composite index."
        exit 1
    fi

    local index_name
    index_name="idx_${table_name}_$(echo "${columns[@]}" | tr ' ' '_')"

    local postgres_container
    postgres_container=$(get_postgres_container_id)
    if [ -z "$postgres_container" ]; then
        echo "No running PostgreSQL container found."
        exit 1
    fi

    local columns_string
    columns_string=$(
        IFS=','
        echo "${columns[*]}"
    )

    echo "Creating composite index $index_name on $table_name ($columns_string)."
    docker exec -u postgres -it "$postgres_container" psql -d postgres -c "CREATE INDEX IF NOT EXISTS $index_name ON $table_name ($columns_string);"
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

    docker exec -u postgres -it "$postgres_container" mkdir -p /tmp
    docker exec -u postgres -it "$postgres_container" psql -d postgres -c "\copy ($query) TO '$output_csv' CSV HEADER;"

    sudo chmod 777 "./InfoCompanies-Data-Model"
    docker cp "$postgres_container:$output_csv" "./InfoCompanies-Data-Model/$(basename "$2")"
}

# Export all unique values at the start of the script
export_all_unique_values() {
    export_unique_values "SELECT DISTINCT industry_sector FROM public.companies" "./InfoCompanies-Data-Model/industry_sector.csv"
    export_unique_values "SELECT DISTINCT city FROM public.companies" "./InfoCompanies-Data-Model/city.csv"
    export_unique_values "SELECT DISTINCT legal_form FROM public.companies" "./InfoCompanies-Data-Model/legal_form.csv"
}

# Main script
case "$ACTION" in
# ./InfoCompanies-Data-Model/db.sh "InfoCompanies-Data-Model/leaders_renamed.csv" transfer_leaders_csv_to_database
transfer_leaders_csv_to_database)
    transfer_csv_to_database "leader" "./InfoCompanies-Data-Model/leaders_renamed.csv" "$(head -1 "./InfoCompanies-Data-Model/leaders_renamed.csv" | tr ';' ',')" ";"
    ;;
transfer_city_csv_to_database)
    transfer_csv_to_database "city" "./InfoCompanies-Data-Model/city.csv" "name" ","
    ;;
transfer_industry_sector_csv_to_database)
    transfer_csv_to_database "industry_sector" "./InfoCompanies-Data-Model/industry_sector.csv" "name" ","
    ;;
# ./InfoCompanies-Data-Model/db.sh "InfoCompanies-Data-Model/final.csv" create_companies_indexes
create_companies_indexes)
    create_indexes "companies" "siren_number" "company_name" "legal_form" "industry_sector" "region" "city" "phone_number" "website" "email" "number_of_employee" "linkedin" "twitter" "facebook" "instagram" "youtube"
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
    cp "./InfoCompanies-Data-Model/$CSV_FILE" "./InfoCompanies-Data-Model/$CSV_FILE.bak"

    output=$(transfer_csv_to_database "companies" "./InfoCompanies-Data-Model/$CSV_FILE" "$(head -1 "./InfoCompanies-Data-Model/$CSV_FILE" | tr ';' ',')" ";" 2>&1)

    if [ $? -ne 0 ]; then
        line_number=$(echo "$output" | grep -oE 'LINE [0-9]+' | grep -oE '[0-9]+')

        if [ -n "$line_number" ]; then
            echo "Error at line $line_number. Deleting the line."
            remove_error_line "$line_number" "./InfoCompanies-Data-Model/$CSV_FILE"
            output=$(transfer_csv_to_database "companies" "./InfoCompanies-Data-Model/$CSV_FILE" "$(head -1 "./InfoCompanies-Data-Model/$CSV_FILE" | tr ';' ',')" ";" 2>&1)
            if [ $? -ne 0 ]; then
                echo "Error during the transfer: $output"
                mv "./InfoCompanies-Data-Model/$CSV_FILE.bak" "./InfoCompanies-Data-Model/$CSV_FILE"
                exit 1
            fi
        else
            echo "Error during the transfer: $output"
            mv "./InfoCompanies-Data-Model/$CSV_FILE.bak" "./InfoCompanies-Data-Model/$CSV_FILE"
            exit 1
        fi
    fi

    echo "Transfer successful."

    transfer_csv_to_database "leader" "./InfoCompanies-Data-Model/leaders_renamed.csv" "$(head -1 "./InfoCompanies-Data-Model/leaders_renamed.csv" | tr ';' ',')" ";"

    # Enable pg_trgm extension
    enable_pg_trgm_extension

    export_all_unique_values

    # Create indexes
    create_indexes "companies" "siren_number" "company_name" "legal_form" "industry_sector" "region" "city" "phone_number" "website" "email" "number_of_employee" "linkedin" "twitter" "facebook" "instagram" "youtube"
    create_indexes "company_seen" "user_id"
    create_indexes "company_seen_company_ids" "company_ids" "company_seen_id"

    # Autocomplete indexes
    create_indexes "city" "name"
    create_indexes "industry_sector" "name"
    create_indexes "legal_form" "name"

    create_indexes "leader" "siren" "company_name" "first_name" "last_name"

    create_composite_index "companies" "region" "city" "industry_sector" "legal_form"
    create_composite_index "companies" "region" "city" "industry_sector"
    create_composite_index "companies" "region" "city" "legal_form"
    create_composite_index "companies" "region" "city"
    create_composite_index "companies" "region" "industry_sector"
    create_composite_index "companies" "region" "legal_form"

    create_composite_index "companies" "city" "industry_sector" "legal_form"
    create_composite_index "companies" "city" "industry_sector"
    create_composite_index "companies" "city" "legal_form"

    create_composite_index "companies" "region" "industry_sector" "legal_form"
    create_composite_index "companies" "industry_sector" "legal_form"

    create_composite_index "companies" "industry_sector" "number_of_employee"

    transfer_csv_to_database "city" "./InfoCompanies-Data-Model/city.csv" "name" ","
    transfer_csv_to_database "industry_sector" "./InfoCompanies-Data-Model/industry_sector.csv" "name" ","
    transfer_csv_to_database "legal_form" "./InfoCompanies-Data-Model/legal_form.csv" "name" ","

    create_trigram_indexes "companies" "company_name"

    python3 InfoCompanies-Data-Model/Final-Sort/Insert-DB/insert.py

    echo "Data insertion into the database successful."
    ;;
esac

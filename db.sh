#!/bin/bash

# On MacOs, you need to create a venv and install the requirements
# python3 -m venv venv
# source .venv/bin/activate
# pip install -r requirements.txt

# Function to display usage
usage() {
    echo "Usage: $0 [options]"
    echo
    echo "If no options are specified, the script will run the default actions."
    echo
    echo "Options:"
    echo "  -h, --help                       Show this help message"
    echo "  -a ACTION, --action ACTION       Specify the action to perform"
    echo "  -f FILE, --file FILE             Specify the CSV file"
    echo "  -b FORMAT, --backup-format FORMAT  Specify the backup format (sql or csv)"
    echo
    echo "Actions:"
    echo "  backup_database                  Backup the database"
    echo "  transfer_leaders_csv_to_database Transfer leaders CSV to database"
    echo "  transfer_city_csv_to_database    Transfer city CSV to database"
    echo "  transfer_industry_sector_csv_to_database Transfer industry sector CSV to database"
    echo "  create_companies_indexes         Create indexes for companies"
    echo "  export_unique_industry_sector    Export unique industry sectors"
    echo "  export_unique_cities             Export unique cities"
    echo "  export_unique_values             Export unique values (requires query and output file)"
    echo
    echo "Example:"
    echo "  sudo -E ./InfoCompanies-Data-Model/db.sh -a backup_database -b csv"
    echo "  sudo -E ./InfoCompanies-Data-Model/db.sh -f './InfoCompanies-Data-Model/final.csv'"
    echo
}

CSV_FILE=""
ACTION=""
BACKUP_FORMAT=""
ARGS=()

# Parse options
while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
    -h | --help)
        usage
        exit 0
        ;;
    -a | --action)
        ACTION="$2"
        shift # past argument
        shift # past value
        ;;
    -f | --file)
        CSV_FILE="$2"
        shift
        shift
        ;;
    -b | --backup-format)
        BACKUP_FORMAT="$2"
        shift
        shift
        ;;
    *)               # positional argument or unknown option
        ARGS+=("$1") # save it in an array for later
        shift        # past argument
        ;;
    esac
done

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
    docker exec -u postgres -i "$postgres_container" psql -d postgres -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"
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

    echo "Transferring the CSV file '$csv_file_path' to the PostgreSQL database."
    docker cp "$csv_file_path" "$postgres_container:$container_csv_file"
    docker exec -u postgres -i "$postgres_container" psql -d postgres -c "\copy $table_name($columns) FROM '$container_csv_file' DELIMITER '$delimiter' CSV HEADER;"
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
        docker exec -u postgres -i "$postgres_container" psql -d postgres -c "CREATE INDEX IF NOT EXISTS idx_${table_name}_${column} ON $table_name ($column);"
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
        docker exec -u postgres -i "$postgres_container" psql -d postgres -c "CREATE INDEX IF NOT EXISTS idx_${table_name}_${column}_trgm ON $table_name USING gin (LOWER($column) gin_trgm_ops);"
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
    docker exec -u postgres -i "$postgres_container" psql -d postgres -c "CREATE INDEX IF NOT EXISTS $index_name ON $table_name ($columns_string);"
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
    local output_file="$2"
    local base_name
    base_name=$(basename "$output_file")
    local output_csv="/tmp/$base_name"

    local postgres_container
    postgres_container=$(get_postgres_container_id)
    if [ -z "$postgres_container" ]; then
        echo "No running PostgreSQL container found."
        exit 1
    fi

    docker exec -u postgres -i "$postgres_container" mkdir -p /tmp
    docker exec -u postgres -i "$postgres_container" psql -d postgres -c "\copy ($query) TO '$output_csv' CSV HEADER;"
    sudo chmod 777 "./InfoCompanies-Data-Model"
    docker cp "$postgres_container:$output_csv" "./InfoCompanies-Data-Model/$base_name"
}

# Function to backup the database
backup_database() {
    local backup_format="${1:-sql}" # Default to 'sql' if no argument is provided

    local postgres_container
    postgres_container=$(get_postgres_container_id)
    if [ -z "$postgres_container" ]; then
        echo "No running PostgreSQL container found."
        exit 1
    fi

    if [ "$backup_format" == "sql" ]; then
        echo "Backing up the PostgreSQL database in SQL format."
        docker exec -u postgres -i "$postgres_container" pg_dump -U postgres -F c -f /tmp/db_backup.dump postgres
        docker cp "$postgres_container:/tmp/db_backup.dump" "./InfoCompanies-Data-Model/db_backup.dump"
        echo "Backup saved to ./InfoCompanies-Data-Model/db_backup.dump"
    elif [ "$backup_format" == "csv" ]; then
        echo "Backing up the PostgreSQL database in CSV format with semicolon delimiters."

        # Define the list of tables to export
        tables=("companies" "leader" "city" "industry_sector" "legal_form")

        for table in "${tables[@]}"; do
            local csv_file="/tmp/${table}_backup.csv"
            docker exec -u postgres -i "$postgres_container" psql -d postgres -c "\copy $table TO '$csv_file' WITH CSV HEADER DELIMITER ';';"
            docker cp "$postgres_container:$csv_file" "./InfoCompanies-Data-Model/${table}_backup.csv"
            echo "Backup of table '$table' saved to ./InfoCompanies-Data-Model/${table}_backup.csv"
        done
    else
        echo "Invalid backup format specified. Use 'sql' or 'csv'."
        exit 1
    fi
}

# Function to export all unique values
export_all_unique_values() {
    export_unique_values "SELECT DISTINCT industry_sector FROM public.companies" "./InfoCompanies-Data-Model/industry_sector.csv"
    export_unique_values "SELECT DISTINCT city FROM public.companies" "./InfoCompanies-Data-Model/city.csv"
    export_unique_values "SELECT DISTINCT legal_form FROM public.companies" "./InfoCompanies-Data-Model/legal_form.csv"
}

# Main script
if [ -z "$ACTION" ]; then
    # No action specified, run default actions
    echo "No action specified. Running default actions."

    # Ensure the CSV file is specified
    if [ -z "$CSV_FILE" ]; then
        echo "Error: CSV file is required for the default action."
        usage
        exit 1
    fi

    sudo chmod +r "$CSV_FILE"
    cp "$CSV_FILE" "$CSV_FILE.bak"

    output=$(transfer_csv_to_database "companies" "$CSV_FILE" "$(head -1 "$CSV_FILE" | tr ';' ',')" ";" 2>&1)

    if [ $? -ne 0 ]; then
        line_number=$(echo "$output" | grep -oE 'LINE [0-9]+' | grep -oE '[0-9]+')

        if [ -n "$line_number" ]; then
            echo "Error at line $line_number. Deleting the line."
            remove_error_line "$line_number" "$CSV_FILE"
            output=$(transfer_csv_to_database "companies" "$CSV_FILE" "$(head -1 "$CSV_FILE" | tr ';' ',')" ";" 2>&1)
            if [ $? -ne 0 ]; then
                echo "Error during the transfer: $output"
                mv "$CSV_FILE.bak" "$CSV_FILE"
                exit 1
            fi
        else
            echo "Error during the transfer: $output"
            mv "$CSV_FILE.bak" "$CSV_FILE"
            exit 1
        fi
    fi

    echo "Transfer successful."

    # Transfer leaders CSV to database
    transfer_csv_to_database "leader" "./InfoCompanies-Data-Model/leaders_renamed.csv" "$(head -1 "./InfoCompanies-Data-Model/leaders_renamed.csv" | tr ';' ',')" ";"

    # Enable pg_trgm extension
    enable_pg_trgm_extension

    # Export unique values
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

    # Create composite indexes
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

    # Transfer additional CSVs
    transfer_csv_to_database "city" "./InfoCompanies-Data-Model/city.csv" "name" ","
    transfer_csv_to_database "industry_sector" "./InfoCompanies-Data-Model/industry_sector.csv" "name" ","
    transfer_csv_to_database "legal_form" "./InfoCompanies-Data-Model/legal_form.csv" "name" ","

    # Create trigram indexes
    create_trigram_indexes "companies" "company_name"

    # Run the Python script
    python3 InfoCompanies-Data-Model/Final-Sort/Insert-DB/insert.py

    echo "Data insertion into the database successful."

else
    # Action specified, handle accordingly
    case "$ACTION" in
    backup_database)
        backup_database "$BACKUP_FORMAT"
        ;;
    transfer_leaders_csv_to_database)
        if [ -z "$CSV_FILE" ]; then
            echo "Error: CSV file is required for this action."
            usage
            exit 1
        fi
        transfer_csv_to_database "leader" "$CSV_FILE" "$(head -1 "$CSV_FILE" | tr ';' ',')" ";"
        ;;
    transfer_city_csv_to_database)
        if [ -z "$CSV_FILE" ]; then
            echo "Error: CSV file is required for this action."
            usage
            exit 1
        fi
        transfer_csv_to_database "city" "$CSV_FILE" "name" ","
        ;;
    transfer_industry_sector_csv_to_database)
        if [ -z "$CSV_FILE" ]; then
            echo "Error: CSV file is required for this action."
            usage
            exit 1
        fi
        transfer_csv_to_database "industry_sector" "$CSV_FILE" "name" ","
        ;;
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
        if [ ${#ARGS[@]} -lt 2 ]; then
            echo "Error: 'export_unique_values' requires a query and output CSV file."
            usage
            exit 1
        fi
        query="${ARGS[0]}"
        output_csv="${ARGS[1]}"
        export_unique_values "$query" "$output_csv"
        ;;
    *)
        echo "Error: Unknown action '$ACTION'."
        usage
        exit 1
        ;;
    esac
fi

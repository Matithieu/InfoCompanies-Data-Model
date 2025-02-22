#!/bin/bash

# On MacOs, you need to create a venv and install the requirements
# python3 -m venv venv
# source .venv/bin/activate
# pip install -q -r requirements.txt

# Function to display usage
usage() {
    echo "Usage: $0 [options]"
    echo
    echo "If no options are specified, the script will run the default actions."
    echo
    echo "Options:"
    echo "  -h, --help                       Show this help message"
    echo "  -a ACTION, --action ACTION       Specify the action to perform"
    echo "  -f FILE, --file FILE              Specify the CSV file"
    echo "  -b FORMAT, --backup-format FORMAT  Specify the backup format (sql or csv)"
    echo
    echo "Actions:"
    echo "  backup_database                  Backup the database"
    echo "  transfer_leaders_csv_to_database Transfer leaders CSV to database"
    echo "  transfer_city_csv_to_database    Transfer city CSV to database"
    echo "  transfer_industry_sector_csv_to_database Transfer industry sector CSV to database"
    echo "  transfer_legal_form_csv_to_database Transfer legal form CSV to database"
    echo "  transfer_region_csv_to_database  Transfer region CSV to database"
    echo "  create_companies_indexes         Create indexes for companies"
    echo "  export_unique_industry_sector    Export unique industry sectors"
    echo "  export_unique_cities             Export unique cities"
    echo "  export_unique_values             Export unique values (requires query and output file)"
    echo "  insert_data                      Insert big data into the database"
    echo "  export_zipped_e2e_data           Export E2E data as SQL dumps and zip the directory"
    echo "  export_e2e_main_data             Export E2E main data as SQL dumps (companies and leader)"
    echo "  export_e2e_sub_data              Export E2E sub data as SQL dumps (industry_sector, city, legal_form)"
    echo "  export_all_unique_values         Export all unique values to CSV files"
    echo "  transport_all_unique_values      Transfer all unique values to the database"
    echo
    echo "Examples:"
    echo "  sudo -E ./InfoCompanies-Data-Model/db.sh -a backup_database -b csv"
    echo "  sudo -E ./InfoCompanies-Data-Model/db.sh -a export_zipped_e2e_data"
    echo "  sudo -E ./InfoCompanies-Data-Model/db.sh -a export_e2e_main_data"
    echo "  sudo -E ./InfoCompanies-Data-Model/db.sh -a export_e2e_sub_data"
    echo "  sudo -E ./InfoCompanies-Data-Model/db.sh -a export_unique_regions"
    echo "  sudo -E ./InfoCompanies-Data-Model/db.sh -a transfer_region_csv_to_database -f \"./InfoCompanies-Data-Model/region.csv\""
    echo "  sudo -E ./InfoCompanies-Data-Model/db.sh -f './InfoCompanies-Data-Model/final.csv'"
    echo "  sudo -E ./InfoCompanies-Data-Model/db.sh -a export_all_unique_values" 
    echo "  sudo -E ./InfoCompanies-Data-Model/db.sh -a transport_all_unique_values"
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
    docker ps --filter "ancestor=postgres:16.4" --format "{{.ID}}"
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

    # This command needs to be run with sudo to give the script the necessary permissions
    echo -e "You might have to enter the sudo password to give the script the necessary permissions.\n"
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

# Function to export unique values to a CSV or SQL file
export_unique_values() {
    local query="$1"
    local output_file="$2"
    local format="${3:-csv}" # Default format is CSV
    local base_name
    base_name=$(basename "$output_file" | sed 's/^e2e_//')
    local postgres_container
    postgres_container=$(get_postgres_container_id)

    if [ -z "$postgres_container" ]; then
        echo "No running PostgreSQL container found."
        exit 1
    fi

    # Ensure the output directory exists
    mkdir -p "$(dirname "$output_file")"

    if [ "$format" == "csv" ]; then
        local output_csv="/tmp/$base_name.csv"
        echo "Exporting unique values for the $base_name table in CSV format..."

        docker exec -u postgres -i "$postgres_container" mkdir -p /tmp
        docker exec -u postgres -i "$postgres_container" psql -d postgres -c "\copy ($query) TO '$output_csv' CSV HEADER;"
        docker cp "$postgres_container:$output_csv" "$output_file"
        echo "Exported CSV file saved to $output_file"
    elif [ "$format" == "sql" ]; then
        echo "Exporting unique values for the $base_name table in SQL format..."
        local temp_table="temp_export"
        local output_sql="$output_file.sql"

        # Create a temporary table with an auto-generated ID
        docker exec -u postgres -i "$postgres_container" psql -d postgres -c "
            DROP TABLE IF EXISTS $temp_table;
            CREATE TABLE $temp_table AS
            SELECT row_number() OVER () AS id, * FROM ($query) AS subquery;
        "

        # Use pg_dump to export the temporary table in SQL format
        docker exec -u postgres -i "$postgres_container" pg_dump -U postgres --data-only --table="$temp_table" postgres >"$output_sql"

        # Clean up the temporary table
        docker exec -u postgres -i "$postgres_container" psql -d postgres -c "DROP TABLE IF EXISTS $temp_table;"

        sed -i '' "s/public\.${temp_table}/public.${base_name}/g" "$output_sql"

        echo "Exported SQL file saved to $output_sql"
    else
        echo "Invalid format specified. Use 'csv' or 'sql'."
        exit 1
    fi
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
        echo "Exporting the backup to ./InfoCompanies-Data-Model/backup/db_backup.dump"
        docker cp "$postgres_container:/tmp/db_backup.dump" "./InfoCompanies-Data-Model/backup/db_backup.dump"
        echo "Backup saved!"
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
    export_unique_values "SELECT DISTINCT industry_sector FROM public.companies" "./InfoCompanies-Data-Model/data/export_docker/industry_sector.csv"
    export_unique_values "SELECT DISTINCT city FROM public.companies" "./InfoCompanies-Data-Model/data/export_docker/city.csv"
    export_unique_values "SELECT DISTINCT legal_form FROM public.companies" "./InfoCompanies-Data-Model/data/export_docker/legal_form.csv"
    export_unique_values "SELECT DISTINCT region FROM public.companies" "./InfoCompanies-Data-Model/data/export_docker/region.csv"
}

transport_all_unique_values() {
    transfer_csv_to_database "city" "./InfoCompanies-Data-Model/data/export_docker/city.csv" "name" ","
    transfer_csv_to_database "industry_sector" "./InfoCompanies-Data-Model/data/export_docker/industry_sector.csv" "name" ","
    transfer_csv_to_database "legal_form" "./InfoCompanies-Data-Model/data/export_docker/legal_form.csv" "name" ","
    transfer_csv_to_database "region" "./InfoCompanies-Data-Model/data/export_docker/region.csv" "name" ","
}

# Function to insert data into the database (big data)
insert_data() {
    echo "Inserting data into the database."

    # List of scripts to run
    scripts=(
        "./InfoCompanies-Data-Model/ETL/load/scrapping/load_big_scrapped_companies.py"
    )

    # Run each script
    for script in "${scripts[@]}"; do
        echo "Running script: $script"
        python3 "$script"
        if [ $? -ne 0 ]; then
            echo "Error running script: $script"
            deactivate
            exit 1
        fi
    done

    echo "Data insertion into the database successful."
    deactivate
}

# When exporting E2E data as SQL dumps, make sure to create the output directory and set the correct permissions:
# sudo chown -R $(whoami):staff ./e2e/e2e_data_sql
#
# Function to export E2E data as SQL dumps
# It exports up to 15MB of data from each table for E2E testing
# It starts by creating a regular table with sampled data from the companies table, exports the data, and then drops the table
export_e2e_data_as_sql() {
    local max_size_mb=15
    local max_size_bytes=$((max_size_mb * 1024 * 1024))
    local tables=("companies" "leader")
    local output_directory="./e2e/e2e_data_sql"

    local postgres_container
    postgres_container=$(get_postgres_container_id)
    if [ -z "$postgres_container" ]; then
        echo -e "${RED}No running PostgreSQL container found. Start the database first.${NC}"
        exit 1
    fi

    mkdir -p "$output_directory"

    echo "Exporting up to $max_size_mb MB of data from each table for E2E testing..."

    for table_name in "${tables[@]}"; do
        local e2e_table="e2e_${table_name}"
        local output_file="$output_directory/e2e_${table_name}.sql"

        echo "Creating a regular table and exporting data from table '$table_name'..."

        # Estimate the number of rows to limit data size to 15MB
        local estimated_row_size
        estimated_row_size=$(docker exec -u postgres -i "$postgres_container" psql -d postgres -t -c "
            SELECT pg_column_size(t.*)
            FROM $table_name t
            LIMIT 1;
        " | tr -d ' ')

        if [ -z "$estimated_row_size" ] || [ "$estimated_row_size" -le 0 ]; then
            echo -e "${RED}Failed to estimate row size for table '$table_name'.${NC}"
            continue
        fi

        local rows_to_export=$((max_size_bytes / estimated_row_size))

        # Create a regular table with sampled data
        docker exec -u postgres -i "$postgres_container" psql -d postgres -c "
            DROP TABLE IF EXISTS $e2e_table;
            CREATE TABLE $e2e_table AS
            SELECT * FROM $table_name LIMIT $rows_to_export;
        "

        # Ensure the regular table is exported properly
        docker exec -u postgres -i "$postgres_container" pg_dump -U postgres -t "$e2e_table" --data-only >"$output_file"

        # Clean up the regular table
        docker exec -u postgres -i "$postgres_container" psql -d postgres -c "DROP TABLE IF EXISTS $e2e_table;"

        # Rename table references inside the SQL dump file
        sed -i '' "s/public\.${e2e_table}/public.${table_name}/g" "$output_file"

        # Set the correct permissions for the output file
        sudo chown -R "$(whoami)":staff "$output_file"

        echo -e "${GREEN}Exported data from '$table_name' to '$output_file' (up to $max_size_mb MB).${NC}"
    done

    echo -e "${GREEN}All E2E data has been exported as SQL dumps to the '$output_directory' directory.${NC}"
}

export_e2e_sub_data() {
    local output_directory="./e2e/e2e_data_sql"

    # Ensure the output directory exists
    mkdir -p "$output_directory"

    echo "Exporting E2E sub-data to $output_directory in SQL format..."
    # Export unique values with 'id' and 'name' instead of 'id' and 'value'
    export_unique_values "SELECT DISTINCT industry_sector AS name FROM public.companies" "$output_directory/e2e_industry_sector" "sql"
    export_unique_values "SELECT DISTINCT city AS name FROM public.companies" "$output_directory/e2e_city" "sql"
    export_unique_values "SELECT DISTINCT legal_form AS name FROM public.companies" "$output_directory/e2e_legal_form" "sql"
    export_unique_values "SELECT DISTINCT region AS name FROM public.companies" "$output_directory/e2e_region" "sql"

    # Set the correct permissions for the output directory
    sudo chown -R "$(whoami):staff" "$output_directory"
    echo "E2E sub-data export completed."
}

zip_e2e_data() {
    local output_directory="./e2e/e2e_data_sql"
    local zip_file="./e2e/data_sql.zip"

    # Ensure the output directory exists
    mkdir -p "$output_directory"

    # Verify that the zip command is available
    if ! command -v zip &> /dev/null; then
        echo "zip command not found. Please install zip and try again."
        exit 1
    fi

    # Verify that there are files to zip
    if [ "$(ls -A "$output_directory")" ]; then
        # Zip the E2E data directory
        zip -r "$zip_file" "$output_directory"
        echo "Zipped E2E data saved to $zip_file"
    else
        echo "No files to zip in the directory '$output_directory'."
    fi
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

    output=$(transfer_csv_to_database "companies" "$CSV_FILE" "$(head -1 "$CSV_FILE" | tr ';' ',')" ";" 2>&1)

    if [ $? -ne 0 ]; then
        line_number=$(echo "$output" | grep -oE 'LINE [0-9]+' | grep -oE '[0-9]+')

        if [ -n "$line_number" ]; then
            echo "Error at line $line_number. Deleting the line."
            # remove_error_line "$line_number" "$CSV_FILE"
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
    transfer_csv_to_database "leader" "./InfoCompanies-Data-Model/ETL/data/output/transform/leaders.csv" "$(head -1 "./InfoCompanies-Data-Model/ETL/data/output/transform/leaders.csv" | tr ';' ',')" ";"

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
    create_indexes "region" "name"

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
    transport_all_unique_values

    # Create trigram indexes
    create_trigram_indexes "companies" "company_name"

    # Run the data insertion function
    insert_data

    echo "Data insertion into the database successful."

else
    # Action specified, handle accordingly
    case "$ACTION" in
    insert_data)
        insert_data
        ;;
    backup_database)
        backup_database "$BACKUP_FORMAT"
        ;;
    export_zipped_e2e_data)
        export_e2e_data_as_sql
        export_e2e_sub_data
        zip_e2e_data
        ;;
    export_e2e_main_data)
        export_e2e_data_as_sql
        ;;
    export_e2e_sub_data)
        export_e2e_sub_data
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
    transfer_legal_form_csv_to_database)
        if [ -z "$CSV_FILE" ]; then
            echo "Error: CSV file is required for this action."
            usage
            exit 1
        fi
        transfer_csv_to_database "legal_form" "$CSV_FILE" "name" ","
        ;;
    transfer_region_csv_to_database)
        if [ -z "$CSV_FILE" ]; then
            echo "Error: CSV file is required for this action."
            usage
            exit 1
        fi
        transfer_csv_to_database "region" "$CSV_FILE" "name" ","
        ;;
    create_companies_indexes)
        create_indexes "companies" "siren_number" "company_name" "legal_form" "industry_sector" "region" "city" "phone_number" "website" "email" "number_of_employee" "linkedin" "twitter" "facebook" "instagram" "youtube"
        ;;
    export_unique_industry_sector)
        export_unique_values "SELECT DISTINCT industry_sector FROM public.companies" "./InfoCompanies-Data-Model/data/export_docker/industry_sector.csv"
        ;;
    export_unique_cities)
        export_unique_values "SELECT DISTINCT city FROM public.companies" "./InfoCompanies-Data-Model/data/export_docker/city.csv"
        ;;
    export_unique_regions)
        export_unique_values "SELECT DISTINCT region AS value FROM public.companies" "./InfoCompanies-Data-Model/data/export_docker/region.csv"
        ;;
    export_all_unique_values)
        export_all_unique_values
        ;;
    transport_all_unique_values)
        transport_all_unique_values
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

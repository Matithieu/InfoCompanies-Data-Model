#!/bin/bash

set -euo pipefail

# Color definitions for logging output
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "$(date +'%Y-%m-%d %H:%M:%S') [INFO] ${BLUE}$*${NC}"
}

log_warn() {
    echo -e "$(date +'%Y-%m-%d %H:%M:%S') [WARN] ${YELLOW}$*${NC}"
}

log_error() {
    echo -e "$(date +'%Y-%m-%d %H:%M:%S') [ERROR] ${RED}$*${NC}"
}

log_success() {
    echo -e "$(date +'%Y-%m-%d %H:%M:%S') [SUCCESS] ${GREEN}$*${NC}"
}


# Function to display usage
usage() {
    echo -e "${BLUE}Usage:${NC}"
    echo -e "  $0 [options]"
    echo -e ""
    echo -e "${YELLOW}Description:${NC}"
    echo -e "  This script manages database operations for the InfoCompanies project using Dockerized PostgreSQL."
    echo -e "  It supports data backup, insertion, export, and transfer of CSV data."
    echo -e ""
    echo -e "${YELLOW}Options:${NC}"
    echo -e "  -h, --help                        Show this help message and exit"
    echo -e "  -a, --action ACTION               Specify the action to perform (see list of actions below)"
    echo -e "  -f, --file FILE                   Path to the CSV file for data transfer"
    echo -e "  -b, --backup-format FORMAT        Specify the backup format (sql or csv)"
    echo -e ""
    echo -e "${YELLOW}Available Actions:${NC}"
    echo -e "  backup_database                   Backup the PostgreSQL database (use -b to set format)"
    echo -e "  export_unique_values              Export unique values from specific columns (requires query and output file)"
    echo -e "  insert_data                       Insert data into the database from predefined ETL scripts"
    echo -e "  export_zipped_e2e_data            Export E2E data as SQL dumps and compress them into a zip archive"
    echo -e "  export_e2e_main_data              Export main E2E data tables (companies, leader) as SQL dumps"
    echo -e "  export_e2e_sub_data               Export sub E2E data (industry_sector, city, legal_form) as SQL dumps"
    echo -e "  zip_final_data                    Compress final data files into zip archives"
    echo -e "  unzip_final_data                  Decompress final data zip archives"
    echo -e "  export_all_unique_values          Export all unique values (city, sector, legal form, region) to CSV files"
    echo -e "  transport_all_unique_values       Transfer exported unique values from CSVs to the database"
    echo -e ""
    echo -e "${YELLOW}Examples:${NC}"
    echo -e "  sudo -E ./InfoCompanies-Data-Model/db.sh -a backup_database -b csv"
    echo -e "  sudo -E ./InfoCompanies-Data-Model/db.sh -a export_zipped_e2e_data"
    echo -e "  sudo -E ./InfoCompanies-Data-Model/db.sh -a export_e2e_main_data"
    echo -e "  sudo -E ./InfoCompanies-Data-Model/db.sh -f './InfoCompanies-Data-Model/final.csv'"
    echo -e "  sudo -E ./InfoCompanies-Data-Model/db.sh -a transport_all_unique_values"
    echo -e ""
    echo -e "${YELLOW}Additional Information:${NC}"
    echo -e "  - Ensure Docker is running and the PostgreSQL container is active."
    echo -e "  - Use 'sudo' if permission issues occur while accessing files or containers."
    echo -e "  - Backup directory: ./InfoCompanies-Data-Model/backup/"
    echo -e "  - Exported data directory: ./InfoCompanies-Data-Model/data/export_docker/"
}


CSV_FILE=""
ACTION=""
BACKUP_FORMAT=""
ARGS=()

# Parse options
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -h|--help)
            usage
            exit 0
            ;;
        -a|--action)
            ACTION="$2"
            shift 2
            ;;
        -f|--file)
            CSV_FILE="$2"
            shift 2
            ;;
        -b|--backup-format)
            BACKUP_FORMAT="$2"
            shift 2
            ;;
        *)
            ARGS+=("$1")
            shift
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
        log_error "No running PostgreSQL container found."
        exit 1
    fi

    log_info "Enabling pg_trgm extension in the PostgreSQL database."
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

    if [ ! -f "$csv_file_path" ]; then
        log_error "The CSV file '$csv_file_path' doesn't exist."
        exit 1
    fi

    log_warn "You might have to enter the sudo password to adjust file permissions."
    sudo chmod +r "$csv_file_path"

    local postgres_container
    postgres_container=$(get_postgres_container_id)
    if [ -z "$postgres_container" ]; then
        log_error "No running PostgreSQL container found."
        exit 1
    fi

    log_info "Transferring the CSV file '$csv_file_path' to the PostgreSQL database."
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
        log_error "No running PostgreSQL container found."
        exit 1
    fi

    for column in "${columns[@]}"; do
        log_info "Creating index idx_${table_name}_${column} on $table_name ($column)."
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
        log_error "No running PostgreSQL container found."
        exit 1
    fi

    for column in "${columns[@]}"; do
        log_info "Creating trigram index idx_${table_name}_${column}_trgm on $table_name ($column)."
        docker exec -u postgres -i "$postgres_container" psql -d postgres -c "CREATE INDEX IF NOT EXISTS idx_${table_name}_${column}_trgm ON $table_name USING gin (LOWER($column) gin_trgm_ops);"
    done
}

# Function to create composite indexes for a given table and set of columns
create_composite_index() {
    local table_name="$1"
    shift
    local columns=("$@")

    if [ ${#columns[@]} -lt 2 ]; then
        log_error "At least two columns are required to create a composite index."
        exit 1
    fi

    local index_name
    index_name="idx_${table_name}_$(echo "${columns[@]}" | tr ' ' '_')"

    local postgres_container
    postgres_container=$(get_postgres_container_id)
    if [ -z "$postgres_container" ]; then
        log_error "No running PostgreSQL container found."
        exit 1
    fi

    local columns_string
    columns_string=$(
        IFS=','
        echo "${columns[*]}"
    )

    log_info "Creating composite index $index_name on $table_name ($columns_string)."
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
        log_error "No running PostgreSQL container found."
        exit 1
    fi

    mkdir -p "$(dirname "$output_file")"

    if [ "$format" == "csv" ]; then
        local output_csv="/tmp/$base_name.csv"
        log_info "Exporting unique values for the $base_name table in CSV format..."

        docker exec -u postgres -i "$postgres_container" mkdir -p /tmp
        docker exec -u postgres -i "$postgres_container" psql -d postgres -c "\copy ($query) TO '$output_csv' CSV HEADER;"
        docker cp "$postgres_container:$output_csv" "$output_file"
        log_success "Exported CSV file saved to $output_file"
    elif [ "$format" == "sql" ]; then
        log_info "Exporting unique values for the $base_name table in SQL format..."
        local temp_table="temp_export"
        local output_sql="$output_file.sql"

        docker exec -u postgres -i "$postgres_container" psql -d postgres -c "
            DROP TABLE IF EXISTS $temp_table;
            CREATE TABLE $temp_table AS
            SELECT row_number() OVER () AS id, * FROM ($query) AS subquery;
        "

        docker exec -u postgres -i "$postgres_container" pg_dump -U postgres --data-only --table="$temp_table" postgres >"$output_sql"

        docker exec -u postgres -i "$postgres_container" psql -d postgres -c "DROP TABLE IF EXISTS $temp_table;"

        sed -i '' "s/public\.${temp_table}/public.${base_name}/g" "$output_sql"

        log_success "Exported SQL file saved to $output_sql"
    else
        log_error "Invalid format specified. Use 'csv' or 'sql'."
        exit 1
    fi
}

# Function to backup the database
backup_database() {
    local backup_format="${1:-sql}" # Default to 'sql'

    local postgres_container
    postgres_container=$(get_postgres_container_id)
    if [ -z "$postgres_container" ]; then
        log_error "No running PostgreSQL container found."
        exit 1
    fi

    if [ "$backup_format" == "sql" ]; then
        log_info "Backing up the PostgreSQL database in SQL format."
        docker exec -u postgres -i "$postgres_container" pg_dump -U postgres -F c -f /tmp/db_backup.dump postgres
        log_info "Exporting the backup to ./InfoCompanies-Data-Model/data/backup/db_backup.dump"
        docker cp "$postgres_container:/tmp/db_backup.dump" "./InfoCompanies-Data-Model/data/backup/db_backup.dump"
        log_success "Backup saved!"
    elif [ "$backup_format" == "csv" ]; then
        log_info "Backing up the PostgreSQL database in CSV format with semicolon delimiters."
        tables=("companies" "leader" "city" "industry_sector" "legal_form")
        for table in "${tables[@]}"; do
            local csv_file="/tmp/${table}_backup.csv"
            docker exec -u postgres -i "$postgres_container" psql -d postgres -c "\copy $table TO '$csv_file' WITH CSV HEADER DELIMITER ';';"
            docker cp "$postgres_container:$csv_file" "./InfoCompanies-Data-Model/data/backup/${table}_backup.csv"
            log_success "Backup of table '$table' saved to ./InfoCompanies-Data-Model/data/backup/${table}_backup.csv"
        done
    else
        log_error "Invalid backup format specified. Use 'sql' or 'csv'."
        exit 1
    fi
}

load_backup() {
    local backup_file="./InfoCompanies-Data-Model/data/backup/db_backup.dump"

    if [ ! -f "$backup_file" ]; then
        log_error "Backup file '$backup_file' does not exist."
        exit 1
    fi

    local postgres_container
    postgres_container=$(get_postgres_container_id)
    if [ -z "$postgres_container" ]; then
        log_error "No running PostgreSQL container found."
        exit 1
    fi

    log_info "Loading the backup from '$backup_file' into the PostgreSQL database."
    docker cp "$backup_file" "$postgres_container:/tmp/db_backup.dump"
    docker exec -u postgres -i "$postgres_container" pg_restore -U postgres -d postgres -c /tmp/db_backup.dump
    log_success "Backup successfully loaded into the database."
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
    log_info "Inserting data into the database."
    scripts=(
        "./InfoCompanies-Data-Model/ETL/load/scrapping/load_big_scrapped_companies.py"
    )
    for script in "${scripts[@]}"; do
        log_info "Running script: $script"
        python3 "$script"
        if [ $? -ne 0 ]; then
            log_error "Error running script: $script"
            deactivate
            exit 1
        fi
    done
    log_success "Data insertion into the database successful."
    deactivate
}

# Function to export E2E data as SQL dumps
export_e2e_data_as_sql() {
    local max_size_mb=15
    local max_size_bytes=$((max_size_mb * 1024 * 1024))
    local tables=("companies" "leader")
    local output_directory="./e2e/e2e_data_sql"

    local postgres_container
    postgres_container=$(get_postgres_container_id)
    if [ -z "$postgres_container" ]; then
        log_error "No running PostgreSQL container found. Start the database first."
        exit 1
    fi

    mkdir -p "$output_directory"
    log_info "Exporting up to $max_size_mb MB of data from each table for E2E testing..."

    for table_name in "${tables[@]}"; do
        local e2e_table="e2e_${table_name}"
        local output_file="$output_directory/e2e_${table_name}.sql"

        log_info "Creating a sampled table for '$table_name'..."
        local estimated_row_size
        estimated_row_size=$(docker exec -u postgres -i "$postgres_container" psql -d postgres -t -c "SELECT pg_column_size(t.*) FROM $table_name t LIMIT 1;" | tr -d ' ')
        if [ -z "$estimated_row_size" ] || [ "$estimated_row_size" -le 0 ]; then
            log_error "Failed to estimate row size for table '$table_name'."
            continue
        fi
        local rows_to_export=$((max_size_bytes / estimated_row_size))
        docker exec -u postgres -i "$postgres_container" psql -d postgres -c "
            DROP TABLE IF EXISTS $e2e_table;
            CREATE TABLE $e2e_table AS
            SELECT * FROM $table_name LIMIT $rows_to_export;
        "
        docker exec -u postgres -i "$postgres_container" pg_dump -U postgres -t "$e2e_table" --data-only >"$output_file"
        docker exec -u postgres -i "$postgres_container" psql -d postgres -c "DROP TABLE IF EXISTS $e2e_table;"
        sed -i '' "s/public\.${e2e_table}/public.${table_name}/g" "$output_file"
        sudo chown -R "$(whoami)":staff "$output_file"
        log_success "Exported data from '$table_name' to '$output_file' (up to $max_size_mb MB)."
    done

    log_success "All E2E data has been exported as SQL dumps to the '$output_directory' directory."
}

export_e2e_sub_data() {
    local output_directory="./e2e/e2e_data_sql"
    mkdir -p "$output_directory"
    log_info "Exporting E2E sub-data to $output_directory in SQL format..."
    export_unique_values "SELECT DISTINCT industry_sector AS name FROM public.companies" "$output_directory/e2e_industry_sector" "sql"
    export_unique_values "SELECT DISTINCT city AS name FROM public.companies" "$output_directory/e2e_city" "sql"
    export_unique_values "SELECT DISTINCT legal_form AS name FROM public.companies" "$output_directory/e2e_legal_form" "sql"
    export_unique_values "SELECT DISTINCT region AS name FROM public.companies" "$output_directory/e2e_region" "sql"
    sudo chown -R "$(whoami):staff" "$output_directory"
    log_success "E2E sub-data export completed."
}

zip_e2e_data() {
    local output_directory="./e2e/e2e_data_sql"
    local zip_file="./e2e/data_sql.zip"
    mkdir -p "$output_directory"

    if ! command -v zip &> /dev/null; then
        log_error "zip command not found. Please install zip and try again."
        exit 1
    fi

    if [ "$(ls -A "$output_directory")" ]; then
        zip -r "$zip_file" "$output_directory"
        log_success "Zipped E2E data saved to $zip_file"
    else
        log_warn "No files to zip in the directory '$output_directory'."
    fi
}

zip_final_data() {
    files_to_zip=(
        # "leaders.csv:./ETL/data/output/transform/leaders.csv"
        # "final.csv:./ETL/data/output/final.csv"
        "backup.dump:./InfoCompanies-Data-Model/data/backup/db_backup.dump"
    )

    if ! command -v zip &> /dev/null; then
        log_error "zip command not found. Please install zip and try again."
        exit 1
    fi

    for entry in "${files_to_zip[@]}"; do
        IFS=":" read -r name file_path <<< "$entry"
        if [ -f "$file_path" ]; then
            local zip_file="${file_path}.zip"
            zip -j "$zip_file" "$file_path"
            log_success "Zipped file saved to $zip_file"
        else
            log_warn "File '$file_path' for '$name' does not exist and will be skipped."
        fi
    done
}

unzip_final_data() {
    files_to_unzip=(
        # "leaders.csv:./ETL/data/output/transform/leaders.csv.zip"
        # "final.csv:./ETL/data/output/final.csv.zip"
        "backup.dump:./InfoCompanies-Data-Model/data/backup/db_backup.dump.zip"
    )

    if ! command -v unzip &> /dev/null; then
        log_error "unzip command not found. Please install unzip and try again."
        exit 1
    fi

    for entry in "${files_to_unzip[@]}"; do
        IFS=":" read -r name zip_file <<< "$entry"
        if [ -f "$zip_file" ]; then
            local output_dir
            output_dir=$(dirname "$zip_file")
            unzip -o "$zip_file" -d "$output_dir"
            log_success "Unzipped file '$zip_file' to '$output_dir'"
        else
            log_warn "Zip file '$zip_file' for '$name' does not exist and will be skipped."
        fi
    done
}


# Main script
if [ -z "$ACTION" ]; then
    if [ "$EUID" -ne 0 ]; then
            log_error "This script must be run as root. Please use 'sudo' to execute it."
            exit 1
    fi

    log_info "No action specified. Running default actions."
    if [ -z "$CSV_FILE" ]; then
        log_error "CSV file is required for the default action."
        usage
        exit 1
    fi

    

    log_info "Transfering the 'companies' CSV file to the PostgreSQL database."
    transfer_csv_to_database "companies" "$CSV_FILE" "$(head -1 "$CSV_FILE" | tr ';' ',')" ";"
    log_success "Transfer of companies data successful."
    

    log_info "Transfering the 'leaders' CSV file to the PostgreSQL database."
    transfer_csv_to_database "leader" "./InfoCompanies-Data-Model/ETL/data/output/transform/leaders.csv" "$(head -1 "./InfoCompanies-Data-Model/ETL/data/output/transform/leaders.csv" | tr ';' ',')" ";"
    log_success "Transfer of leaders data successful."

    log_info "Creating indexes for the tables."
    enable_pg_trgm_extension
    export_all_unique_values
    create_indexes "companies" "siren_number" "company_name" "legal_form" "industry_sector" "region" "city" "phone_number" "website" "email" "number_of_employee" "linkedin" "twitter" "facebook" "instagram" "youtube"
    create_indexes "company_seen" "user_id"
    create_indexes "company_seen_company_ids" "company_ids" "company_seen_id"
    create_indexes "city" "name"
    create_indexes "industry_sector" "name"
    create_indexes "legal_form" "name"
    create_indexes "region" "name"
    create_indexes "leader" "siren" "company_name" "first_name" "last_name"
    log_success "Indexes creation successful."

    log_info "Creating composite indexes for the 'companies' table."
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
    transport_all_unique_values
    create_trigram_indexes "companies" "company_name"
    log_success "Composite indexes creation successful."

    log_info "Inserting scrapped data into the database."
    insert_data
    log_success "Data insertion into the database successful."
else
    case "$ACTION" in
        insert_data)
            insert_data
            ;;
        backup_database)
            backup_database "$BACKUP_FORMAT"
            ;;
        load_backup)
            load_backup
            ;;
        zip_final_data)
            zip_final_data
            ;;
        unzip_final_data)
            unzip_final_data
            ;;
        export_zipped_e2e_data)
            export_e2e_data_as_sql
            export_e2e_sub_data
            zip_e2e_data
            ;;
        transfer_csv_to_database)
            if [ ${#ARGS[@]} -lt 4 ]; then
                log_error "Error: 'transfer_csv_to_database' requires table name, CSV file, columns, and delimiter."
                usage
                exit 1
            fi
            transfer_csv_to_database "${ARGS[0]}" "${ARGS[1]}" "${ARGS[2]}" "${ARGS[3]}"
            ;;
        create_indexes)
            if [ ${#ARGS[@]} -lt 2 ]; then
                log_error "Error: 'create_indexes' requires a table name and at least one column."
                usage
                exit 1
            fi
            create_indexes "${ARGS[0]}" "${ARGS[@]:1}"
            ;;
        export_all_unique_values)
            export_all_unique_values
            ;;
        transport_all_unique_values)
            transport_all_unique_values
            ;;
        export_unique_values)
            if [ ${#ARGS[@]} -lt 2 ]; then
                log_error "Error: 'export_unique_values' requires a query and output CSV file."
                usage
                exit 1
            fi
            query="${ARGS[0]}"
            output_csv="${ARGS[1]}"
            export_unique_values "$query" "$output_csv"
            ;;
        *)
            log_error "Unknown action '$ACTION'."
            usage
            exit 1
            ;;
    esac
fi

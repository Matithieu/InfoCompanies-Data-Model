#!/bin/bash

set -euo pipefail

# shellcheck disable=SC1091
source ./scripts/util.sh


# Transfers data from a CSV file to the database.
# Usage: transfer_csv_to_database <csv_file> <database_name> <table_name>
# Arguments:
#   csv_file      - Path to the CSV file to be imported.
#   database_name - Name of the target database.
#   table_name    - Name of the target table in the database.
# This function handles the process of loading CSV data into the specified database table.
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

    local postgres_container
    postgres_container=$(get_infocompanies_data_model_postgres_container)

    log_info "Transferring the CSV file '$csv_file_path' to the PostgreSQL database."

    docker cp "$csv_file_path" "$postgres_container:$container_csv_file"
    docker exec -u postgres -i "$postgres_container" psql -d postgres -c "COPY $table_name($columns) FROM '$container_csv_file' DELIMITER '$delimiter' CSV HEADER;"
    
    log_success "Transfer of '$csv_file_path' to the database table '$table_name' completed successfully."
}


# Main script execution starts here
log_info "Loading 'companies' and 'leaders' CSV data into the database."
transfer_csv_to_database "companies" "./final.csv" "$(head -1 "./final.csv" | tr ';' ',')" ";"
transfer_csv_to_database "leaders" "./leaders.csv" "$(head -1 "./leaders.csv" | tr ';' ',')" ";"

log_info "Inserting scrapped data into the database."
python3 "./scripts/load_scrapped_companies.py"

log_info "Exporting data for autocompletes from the database."
export_unique_values "SELECT DISTINCT industry_sector FROM public.companies" "./data/export_docker/industry_sector.csv"
export_unique_values "SELECT DISTINCT city FROM public.companies" "./data/export_docker/city.csv"
export_unique_values "SELECT DISTINCT legal_form FROM public.companies" "./data/export_docker/legal_form.csv"
export_unique_values "SELECT DISTINCT region FROM public.companies" "./data/export_docker/region.csv"


log_info "Loading data for autocompletes into the database."
transfer_csv_to_database "city" "./data/export_docker/city.csv" "name" ","
transfer_csv_to_database "industry_sector" "./data/export_docker/industry_sector.csv" "name" ","
transfer_csv_to_database "legal_form" "./data/export_docker/legal_form.csv" "name" ","
transfer_csv_to_database "region" "./data/export_docker/region.csv" "name" ","


log_success "Data loading and export completed successfully."
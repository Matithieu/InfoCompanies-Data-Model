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

    if [ ! -f "$csv_file_path" ]; then
        log_error "The CSV file '$csv_file_path' doesn't exist."
        exit 1
    fi

    log_info "Copying data from '$csv_file_path' to the database table '$table_name'..."

    psql -d postgres -c "\copy $table_name($columns) FROM '$csv_file_path' DELIMITER '$delimiter' CSV HEADER;"
    
    log_success "Transfer of '$csv_file_path' to the database table '$table_name' completed successfully."
}

# Main script execution starts here
log_info "Loading 'companies' and 'leaders' CSV data into the database."
companies_header=$(head -n 1 "./final.csv" | tr ';' ',')
leaders_header=$(head -n 1 "./leaders.csv" | tr ';' ',')

transfer_csv_to_database "companies" "./final.csv" "$companies_header" ";"
transfer_csv_to_database "leaders" "./leaders.csv" "$leaders_header" ";"

log_success "CSV data loading completed successfully."
#!/bin/bash

set -euo pipefail

# shellcheck disable=SC1091
source ./scripts/util.sh

# Function to export unique values to a CSV or SQL file
export_unique_values() {
    local query="$1"
    local output_file="$2"
    local format="${3:-csv}" # Default format is CSV
    local base_name
    base_name=$(basename "$output_file")

    mkdir -p "$(dirname "$output_file")"

    if [ "$format" == "csv" ]; then
        log_info "Exporting unique values for the $base_name table in CSV format..."

        psql -d postgres -c "\copy ($query) TO '$output_file' CSV HEADER;"
        log_success "Exported CSV file saved to $output_file"

    elif [ "$format" == "sql" ]; then
        log_info "Exporting unique values for the $base_name table in SQL format..."

        local temp_table="temp_export"
        local output_sql="$output_file.sql"

        psql -d postgres -c "
            DROP TABLE IF EXISTS $temp_table;
            CREATE TABLE $temp_table AS
            SELECT row_number() OVER () AS id, * FROM ($query) AS subquery;
        "

        pg_dump -U postgres --data-only --table="$temp_table" postgres >"$output_sql"
        psql -d postgres -c "DROP TABLE IF EXISTS $temp_table;"

        log_success "Exported SQL file saved to $output_sql"
    else
        log_error "Invalid format specified. Use 'csv' or 'sql'."
        exit 1
    fi
}

# Transfers data from a CSV file to the database.
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

# Main execution
log_info "Exporting data for autocompletes from the database."
export_unique_values "SELECT DISTINCT industry_sector FROM public.companies WHERE industry_sector IS NOT NULL" "./data/export_docker/industry_sector.csv"
export_unique_values "SELECT DISTINCT city FROM public.companies WHERE city IS NOT NULL" "./data/export_docker/city.csv"
export_unique_values "SELECT DISTINCT legal_form FROM public.companies WHERE legal_form IS NOT NULL" "./data/export_docker/legal_form.csv"
export_unique_values "SELECT DISTINCT region FROM public.companies WHERE region IS NOT NULL" "./data/export_docker/region.csv"

log_info "Loading data for autocompletes into the database."
transfer_csv_to_database "city" "./data/export_docker/city.csv" "name" ","
transfer_csv_to_database "industry_sector" "./data/export_docker/industry_sector.csv" "name" ","
transfer_csv_to_database "legal_form" "./data/export_docker/legal_form.csv" "name" ","
transfer_csv_to_database "region" "./data/export_docker/region.csv" "name" ","

log_success "Autocomplete data export and loading completed successfully."

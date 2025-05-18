#!/bin/bash

set -euo pipefail

# shellcheck disable=SC1091
source ./scripts/util.sh
output_directory="./data/e2e"
sql_output_directory="${output_directory}/sql"


# Function to export E2E data as SQL dumps 
export_e2e_data_as_sql() {
    local max_size_mb=15
    local max_size_bytes=$((max_size_mb * 1024 * 1024))
    local tables=("companies" "leaders")

    local postgres_container
    postgres_container=$(get_infocompanies_data_model_postgres_container)

    log_info "Exporting up to '$max_size_mb' MB of data from each table for E2E testing..."

    for table_name in "${tables[@]}"; do
        local e2e_table="e2e_${table_name}"
        local output_file="$sql_output_directory/e2e_${table_name}.sql"

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

        log_success "Exported data from '$table_name' to '$output_file' (up to $max_size_mb MB)."
    done

    log_success "All E2E data has been exported as SQL dumps to the '$sql_output_directory' directory."
}

export_e2e_sub_data() {
    log_info "Exporting E2E sub-data to $sql_output_directory in SQL format..."

    export_unique_values "SELECT DISTINCT industry_sector AS name FROM public.companies" "$sql_output_directory/e2e_industry_sector" "sql"
    export_unique_values "SELECT DISTINCT city AS name FROM public.companies" "$sql_output_directory/e2e_city" "sql"
    export_unique_values "SELECT DISTINCT legal_form AS name FROM public.companies" "$sql_output_directory/e2e_legal_form" "sql"
    export_unique_values "SELECT DISTINCT region AS name FROM public.companies" "$sql_output_directory/e2e_region" "sql"
    
    log_success "E2E sub-data export completed."
}

gzip_e2e_data() {
    local gzip_file="$output_directory/e2e_data_sql.tar.gz"

    if ! command -v tar &> /dev/null || ! command -v gzip &> /dev/null; then
        log_error "tar or gzip command not found. Please install them and try again."
        exit 1
    fi

    if [ "$(ls -A "$output_directory")" ]; then
        tar -czf "$gzip_file" -C "$output_directory" .
        log_success "Gzipped E2E data saved to $gzip_file"
    else
        log_error "No files to gzip in the directory '$output_directory'."
    fi
}


# Main script
log_info "Exporting E2E data as SQL dumps..."
mkdir -p "$sql_output_directory"

log_info "Exporting E2E data as SQL"
export_e2e_data_as_sql

log_info "Exporting E2E sub-data as SQL"
export_e2e_sub_data

log_info "Gzipping E2E data"
gzip_e2e_data


log_success "E2E data export and compression completed successfully."
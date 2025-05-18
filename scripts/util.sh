#!/bin/bash

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


get_infocompanies_data_model_postgres_container() {
    echo "infocompanies-data-model-postgres"
}

# Function to set up and activate a Python virtual environment
setup_virtual_environment() {
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
        log_info "Virtual environment created."
    fi

    # Activate the virtual environment
    # shellcheck disable=SC1091
    source .venv/bin/activate
    log_info "Virtual environment activated."

    # Install required Python packages
    if [ -f "requirements-dev.in" ]; then
        pip install -r requirements-dev.in --quiet
        log_info "Python dependencies installed."
    else
        log_warn "requirements-dev.in not found. Skipping dependency installation."
    fi
}


# Function to export unique values to a CSV or SQL file
export_unique_values() {
    local query="$1"
    local output_file="$2"
    local format="${3:-csv}" # Default format is CSV
    local base_name
    base_name=$(basename "$output_file" | sed 's/^e2e_//')
    local postgres_container
    postgres_container=$(get_infocompanies_data_model_postgres_container)

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



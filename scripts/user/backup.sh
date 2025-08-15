#!/bin/bash

set -euo pipefail

# shellcheck disable=SC1091
source ./scripts/util.sh


backup_database() {
    local backup_format="${1:-sql}"
    local backup_dir="./data/backup"

    local postgres_container
    postgres_container=$(get_infocompanies_data_model_postgres_container)

    if [ "$backup_format" == "sql" ]; then
        log_info "Backing up the PostgreSQL database in SQL format."

        docker exec -u postgres -i "$postgres_container" pg_dump -U postgres -F c -f /tmp/db_backup.dump postgres
        log_info "Exporting the backup to \"$backup_dir/db_backup.dump\""
        docker cp "$postgres_container:/tmp/db_backup.dump" "$backup_dir/db_backup.dump"

        log_success "Backup saved!"
    elif [ "$backup_format" == "csv" ]; then
        log_info "Backing up the PostgreSQL database in CSV format with semicolon delimiters."
        
        tables=("companies" "leader" "city" "industry_sector" "legal_form")

        for table in "${tables[@]}"; do
            local csv_file="/tmp/${table}_backup.csv"
            docker exec -u postgres -i "$postgres_container" psql -d postgres -c "\copy $table TO '$csv_file' WITH CSV HEADER DELIMITER ';';"
            docker cp "$postgres_container:$csv_file" "$backup_dir/${table}_backup.csv"
            log_success "Backup of table '$table' saved to $backup_dir/${table}_backup.csv"
        done
    else
        log_error "Invalid backup format specified. Use 'sql' or 'csv'."
        exit 1
    fi
}

load_backup() {
    local backup_file="./data/backup/db_backup.dump"

    if [ ! -f "$backup_file" ]; then
        log_error "Backup file '$backup_file' does not exist."
        exit 1
    fi

    local postgres_container
    postgres_container=$(get_infocompanies_data_model_postgres_container)

    log_info "Loading the backup from '$backup_file' into the PostgreSQL database."

    docker cp "$backup_file" "$postgres_container:/tmp/db_backup.dump"
    docker exec -u postgres -i "$postgres_container" pg_restore -U postgres -d postgres -c /tmp/db_backup.dump

    log_success "Backup successfully loaded into the database."
}


gzip_backup() {
  local file_path="./data/backup/db_backup.dump"
  local gzip_file="${file_path}.gz"

  if ! command -v gzip &> /dev/null; then
    log_error "gzip command not found. Please install gzip and try again."
    exit 1
  fi

  if [ -f "$file_path" ]; then
    gzip -c "$file_path" > "$gzip_file"
    log_success "Gzipped file saved to $gzip_file"
  else
    log_warn "File '$file_path' does not exist and will be skipped."
  fi
}

gunzip_backup() {
  local gzip_file="./data/backup/db_backup.dump.gz"

  if ! command -v gunzip &> /dev/null; then
    log_error "gunzip command not found. Please install gunzip and try again."
    exit 1
  fi

  if [ -f "$gzip_file" ]; then
    gunzip -k "$gzip_file"
    log_success "Gunzipped file '$gzip_file' to '${gzip_file%.gz}'"
  else
    log_warn "Gzip file '$gzip_file' does not exist and will be skipped."
  fi
}

case "$1" in
  backup_database)
    BACKUP_FORMAT="${2:-sql}"
    backup_database "$BACKUP_FORMAT"
    ;;
  load_backup)
    load_backup
    ;;
  gzip_backup)
    gzip_backup
    ;;
  gunzip_backup)
    gunzip_backup
    ;;
  *)
    echo "Usage: $0 {backup_database|load_backup|gzip_backup|gunzip_backup} [format]"
    exit 1
    ;;
esac
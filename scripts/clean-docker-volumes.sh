#!/bin/bash

set -euo pipefail

# shellcheck disable=SC1091
source ./scripts/util.sh
volume="$(get_infocompanies_data_model_postgres_volume)"


log_info "Stopping Docker containers..."
docker compose down

log_info "Cleaning up Docker volume..."
docker volume rm -f "$volume"

log_success "Docker volume cleaned up."
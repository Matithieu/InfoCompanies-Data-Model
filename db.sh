#!/bin/bash

set -euo pipefail

# shellcheck disable=SC1091
source ./scripts/util.sh


if [ "$EUID" -ne 0 ]; then
    echo "This script must be run as root. Please use sudo."
    exit 1
fi


# Main script
# ./scripts/pull-csv.sh

docker compose up -d --quiet-pull


log_info "Initializing the database."
cd ./schema
alembic upgrade head

log_info "Executing Database.py"
PYTHONPATH=. python3 app/database/database.py
cd ..


./scripts/load-csv-to-database.sh
./scripts/export-e2e-data.sh

docker compose down


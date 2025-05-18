#!/bin/bash

set -euo pipefail

# shellcheck disable=SC1091
source ./scripts/util.sh


# Main script
if [[ "${GITHUB_CI:-}" == "true" ]]; then
  ./scripts/pull-csv.sh
fi

docker compose up -d --quiet-pull
sleep 2

log_info "Initializing the database."
cd ./schema
alembic upgrade head

log_info "Executing Database.py"
PYTHONPATH=. python3 app/database/database.py
cd ..


./scripts/load-csv-to-database.sh
./scripts/export-e2e-data.sh

docker compose down


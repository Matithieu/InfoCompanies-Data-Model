#!/bin/bash

set -euo pipefail

# shellcheck disable=SC1091
source ./scripts/util.sh

log_info "Initializing the database."
cd ./schema
alembic upgrade head
log_info "Database initialized."
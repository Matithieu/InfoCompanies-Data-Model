#!/bin/bash

set -euo pipefail

# shellcheck disable=SC1091
source ./scripts/util.sh


# Pull the CSVs to insert
log_info "Pulling the CSVs..."
curl -u "$NEXUS_USERNAME:$NEXUS_PASSWORD" -O "$NEXUS_URL/repository/datasets/versions/v1.0/leaders.csv.gz"
curl -u "$NEXUS_USERNAME:$NEXUS_PASSWORD" -O "$NEXUS_URL/repository/datasets/versions/v1.0/final.csv.gz"
curl -u "$NEXUS_USERNAME:$NEXUS_PASSWORD" -O "$NEXUS_URL/repository/datasets/versions/v1.0/fichier_combine_updated_big_fixed.csv.gz"
log_success "CSV files pulled successfully."

# Uncompress the CSVs
log_info "Uncompressing the CSVs..."
gunzip leaders.csv.gz
gunzip final.csv.gz
gunzip fichier_combine_updated_big_fixed.csv.gz

log_success "CSV files uncompressed successfully."
#!/bin/bash

set -euo pipefail

# shellcheck disable=SC1091
source ./scripts/util.sh
# shellcheck disable=SC1091
source .env

# Reminder: we use the native Nexus port and not the Docker one
NEXUS_CSV_URL="${NEXUS_URL}/repository/datasets"
USERNAME_WITH_PASSWORD=$(build_nexus_username_with_password "$NEXUS_USERNAME" "$NEXUS_PASSWORD")

# TODO: Change that to be only done by the CI
FINAL_TAG="0.1"
LEADER_TAG="0.1"
FICHIER_COMBINE_TAG="0.1"

LEADER_CSV="leaders-$LEADER_TAG.csv.gz"
FINAL_CSV="final-$FINAL_TAG.csv.gz"
FICHIER_COMBINE_CSV="fichier_combine_updated_big_fixed-$FICHIER_COMBINE_TAG.csv.gz"

# Pull the CSVs to insert
log_info "Pulling the CSVs..."
curl -u "$USERNAME_WITH_PASSWORD" -O "$NEXUS_CSV_URL/$LEADER_CSV"
curl -u "$USERNAME_WITH_PASSWORD" -O "$NEXUS_CSV_URL/$FINAL_CSV"
curl -u "$USERNAME_WITH_PASSWORD" -O "$NEXUS_CSV_URL/$FICHIER_COMBINE_CSV"
log_success "CSV files pulled successfully."

# Uncompress the CSVs
log_info "Uncompressing the CSVs..."
gunzip "$LEADER_CSV"
gunzip "$FINAL_CSV"
gunzip "$FICHIER_COMBINE_CSV"

# Rename files to remove version tags
mv "leaders-$LEADER_TAG.csv" "leaders.csv"
mv "final-$FINAL_TAG.csv" "final.csv"
mv "fichier_combine_updated_big_fixed-$FICHIER_COMBINE_TAG.csv" "fichier_combine_updated_big_fixed.csv"

log_success "CSV files uncompressed successfully."
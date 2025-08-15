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

echo "Pushing CSVs to Nexus..."
curl -u "$USERNAME_WITH_PASSWORD" \
     --upload-file ./final.csv.gz \
     "$NEXUS_CSV_URL/final-${FINAL_TAG}.csv.gz"

curl -u "$USERNAME_WITH_PASSWORD" \
     --upload-file ./leaders.csv.gz \
     "$NEXUS_CSV_URL/leaders-${LEADER_TAG}.csv.gz"

curl -u "$USERNAME_WITH_PASSWORD" \
     --upload-file ./fichier_combine_updated_big_fixed.csv.gz \
     "$NEXUS_CSV_URL/fichier_combine_updated_big_fixed-${FICHIER_COMBINE_TAG}.csv.gz"
echo "CSV files pushed successfully."
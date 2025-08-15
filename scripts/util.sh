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

# Hardcoded names in Docker
get_infocompanies_data_model_postgres_container() {
    echo "infocompanies-data-model-postgres"
}

# The volume name is different from the container name
get_infocompanies_data_model_postgres_volume() {
    echo "infocompanies-data-model_postgres-data"
}

# Nexus
build_nexus_url_with_port() {
    local port="$1"
    if [[ -z "$port" ]]; then
        echo "$NEXUS_URL"
    else
        echo "${NEXUS_URL}:${port}"
    fi
}

build_nexus_username_with_password() {
    local username="$1"
    local password="$2"
    if [[ -z "$username" || -z "$password" ]]; then
        echo ""
    else
        echo "${username}:${password}"
    fi
}

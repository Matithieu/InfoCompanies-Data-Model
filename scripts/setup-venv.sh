#!/bin/bash

set -euo pipefail

# shellcheck disable=SC1091
source ./scripts/util.sh


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

    local requirements_folder="./requirements"
    local requirements_files=(
        "$requirements_folder/lint.sh"
        "$requirements_folder/build.sh"
    )

    # Install requirements
    for requirements_file in "${requirements_files[@]}"; do
        if [ -f "$requirements_file" ]; then
            pip install -r "$requirements_file"
            log_success "Installed requirements from $requirements_file."
        else
            log_warn "Requirements file $requirements_file not found."
        fi
    done
}

setup_virtual_environment
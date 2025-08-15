FROM postgres:16.4

# Install Python & dependencies for Alembic
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-venv python3-pip postgresql-client \
    && python3 -m venv /opt/venv \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install as root (postgres user cannot write to venv yet)
COPY requirements/build.in /tmp/requirements.in
RUN pip install --no-cache-dir -r /tmp/requirements.in

# Copy app code
WORKDIR /app
COPY schema ./schema
COPY scripts ./scripts

# Make migration script executable
COPY ./scripts/docker/run-migrations.sh /docker-entrypoint-initdb.d/01_run_migrations.sh
RUN chmod +x /docker-entrypoint-initdb.d/01_run_migrations.sh

# Switch to postgres user (final step)
USER postgres

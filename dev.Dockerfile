# ===============================
# Builder stage – preload database
# ===============================
FROM postgres:16.4 AS builder

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=root
ENV POSTGRES_DB=postgres
ENV PGDATA=/var/lib/postgresql/data

# Install Python & dependencies for Alembic
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-venv python3-pip postgresql-client \
 && python3 -m venv /opt/venv \
 && rm -rf /var/lib/apt/lists/*

ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install
COPY requirements/build.in /tmp/requirements.in
RUN pip install --no-cache-dir -r /tmp/requirements.in

# Copy app code and CSVs
WORKDIR /app
COPY schema ./schema
COPY scripts ./scripts
COPY scripts/setup-db.sh /app/setup-db.sh
COPY final.csv leaders.csv fichier_combine_updated_big_fixed.csv ./

# Make ./data writable by postgres user
RUN mkdir -p /app/data && chown -R postgres:postgres /app/data

# Start Postgres for migrations and CSV loading
USER postgres
RUN /app/setup-db.sh

# ===============================
# Final image – production-ready
# ===============================
FROM postgres:16.4

# Copy preloaded, vacuumed database
COPY --from=builder /var/lib/postgresql/data /var/lib/postgresql/data

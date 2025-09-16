# ===============================
# Builder stage – preload database
# ===============================
FROM postgres:16.4 AS builder

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=root
ENV POSTGRES_DB=postgres
ENV PGDATA=/var/lib/postgresql/data

# Install Node.js and Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
 && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
 && apt-get install -y nodejs npm postgresql-client python3 python3-pip python3-venv \
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

# Install dependencies
RUN npm install -g --no-fund pnpm@10.10.0
WORKDIR /app/schema
RUN pnpm install --frozen-lockfile
WORKDIR /app

# Make ./data writable by postgres user
RUN mkdir -p /app/data && chown -R postgres:postgres /app/data
RUN chown -R postgres:postgres /app/schema/

# Start Postgres for migrations and CSV loading
USER postgres
RUN /app/setup-db.sh

# ===============================
# Final image – production-ready
# ===============================
FROM postgres:16.4

# Copy preloaded, vacuumed database
COPY --from=builder /var/lib/postgresql/data /var/lib/postgresql/data

#!/bin/bash
set -e

# Start Postgres in background
docker-entrypoint.sh postgres &

# Wait for Postgres to be ready
echo "Waiting for Postgres..."
sleep 5

export PGHOST=localhost
export PGUSER=postgres
export PGPASSWORD=root

# Test connection
psql -d postgres -c "SELECT 1;"

# Run migrations
cd /app/schema
alembic upgrade head
PYTHONPATH=. python ./app/database/database.py
cd /app

psql -v ON_ERROR_STOP=1 --username="$POSTGRES_USER" <<EOSQL
        ALTER SYSTEM SET max_wal_size = '6GB';
        ALTER SYSTEM SET checkpoint_timeout = '30min';
        ALTER SYSTEM SET synchronous_commit = off;
        ALTER SYSTEM SET fsync = off;
        ALTER SYSTEM SET full_page_writes = off;
EOSQL

# Reload Postgres configuration
psql -d postgres -c "SELECT pg_reload_conf();"

# Load CSV
/app/scripts/load-csv-to-database.sh

# Reset performance settings
psql -d postgres -v ON_ERROR_STOP=1 <<EOSQL
        ALTER SYSTEM RESET max_wal_size;
        ALTER SYSTEM RESET checkpoint_timeout;
        ALTER SYSTEM RESET synchronous_commit;
        ALTER SYSTEM RESET fsync;
        ALTER SYSTEM RESET full_page_writes;
EOSQL

# Reload Postgres configuration
psql -d postgres -c "SELECT pg_reload_conf();"

# Vacuum and analyze
psql -d postgres -c "VACUUM FULL;"
psql -d postgres -c "ANALYZE;"

# Stop Postgres
pg_ctl -D "$PGDATA" -m fast stop

# Clean temporary files
rm -rf "$PGDATA"/pg_wal/archive_status/* "$PGDATA"/pg_stat_tmp/* "$PGDATA"/pg_logical/snapshots/* "$PGDATA"/pg_snapshots/*

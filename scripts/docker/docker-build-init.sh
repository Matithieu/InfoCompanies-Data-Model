#!/bin/bash
set -e

echo ">>> Initializing Postgres data at build time..."

# Init database cluster
initdb -D /var/lib/postgresql/data

# Prepend Docker subnet access to pg_hba.conf
# This ensures it is checked BEFORE any default scram-sha-256 lines
sed -i "1ihost all all 172.19.0.0/16 md5" /var/lib/postgresql/data/pg_hba.conf

# Start Postgres on IPv4 localhost
pg_ctl -D /var/lib/postgresql/data \
  -o "-c listen_addresses='*' -c unix_socket_directories='/var/run/postgresql'" \
  -w start

# Wait until Postgres is ready
until pg_isready -U postgres -h 127.0.0.1 -p 5432; do
    echo "Waiting for Postgres to be ready..."
    sleep 1
done

# Before running migrations / CSV load
psql -v ON_ERROR_STOP=1 --username=postgres <<-EOSQL
    ALTER SYSTEM SET max_wal_size = '6GB';
    ALTER SYSTEM SET checkpoint_timeout = '30min';
    ALTER SYSTEM SET synchronous_commit = off;
    ALTER SYSTEM SET fsync = off;
    ALTER SYSTEM SET full_page_writes = off;
EOSQL
pg_ctl -D /var/lib/postgresql/data reload

# Apply migrations
export DATABASE_URL=postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@127.0.0.1:5432/$POSTGRES_DB
cd /app/schema
PYTHONPATH=/app alembic upgrade head

# Populate with CSV data
PYTHONPATH=/app python /app/app/database/database.py
cd ..
/app/scripts/load-csv-to-database.sh

# Restore safer defaults
psql -v ON_ERROR_STOP=1 --username=postgres <<-EOSQL
    ALTER SYSTEM RESET max_wal_size;
    ALTER SYSTEM RESET checkpoint_timeout;
    ALTER SYSTEM RESET synchronous_commit;
    ALTER SYSTEM RESET fsync;
    ALTER SYSTEM RESET full_page_writes;
EOSQL
pg_ctl -D /var/lib/postgresql/data reload

# Stop Postgres
pg_ctl -D /var/lib/postgresql/data -m fast -w stop

echo ">>> Database populated and baked into image."

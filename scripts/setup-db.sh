#!/bin/bash

# What we do here is ugly. We start Postgres, run migrations and load CSV data. We "bake" an image
# with a full database, so that when we start Postgres for real, it's already populated.
#
# We should decouple this logic from the Postgres image.
# The data from the CSV is static, so we don't need to load it every time we start the DB.
#
# On way to do would be to do like in production: having two containers, one for Postgres
# with baked data in it, and one to run the migrations.
#
# When loading the CSV, we need the tables to be created. We launch the embedded migrations, load the CSVs and build the image.
# Then, the migration container run the migrations on top of that image. Prisma creates a table to track the migrations.


set -e

# Start Postgres in background
docker-entrypoint.sh postgres \
  -c max_wal_size=6GB \
  -c min_wal_size=1GB \
  -c checkpoint_timeout=30min \
  -c checkpoint_completion_target=0.9 \
  -c synchronous_commit=off \
  -c fsync=off \
  -c full_page_writes=off \
  -c wal_level=minimal \
  -c max_wal_senders=0 \
  &

# Wait for Postgres to be ready
echo "Waiting for Postgres..."
until pg_isready -h localhost -p 5432 -U "$POSTGRES_USER"; do
  echo "Waiting for Postgres..."
  sleep 1
done
echo "Postgres is ready!"

export DATABASE_URL="postgresql://postgres:root@localhost:5432/postgres"

# Test connection
psql -d postgres -c "SELECT 1;"

# Run migrations (creates all tables + indexes)
cd /app/schema
pnpm exec prisma migrate deploy
pnpm exec prisma generate
cd /app

# In order to speed up the CSV data load, we drop all non-PK indexes before loading,
# then recreate them after. This is much faster than maintaining the indexes during the load.
echo "Exporting current indexes to backup file..."
psql -d postgres -f /app/scripts/sql/export-indexes.sql

echo "Dropping all non-PK indexes to optimize bulk data loading..."
psql -d postgres -f /app/scripts/sql/drop-indexes-from-backup.sql

echo "Loading CSV data into database (without indexes for maximum speed)..."
/app/scripts/load-csv-to-database.sh

echo "Analyzing tables after CSV load..."
psql -d postgres -c "ANALYZE public.companies;"
psql -d postgres -c "ANALYZE public.leaders;"

echo "Creating temporary index on siren_number for UPDATE optimization..."
psql -d postgres -f /app/scripts/sql/create-temp-siren-index.sql

echo "Updating companies with scraped data..."
python3 "./scripts/load_scrapped_companies.py"

echo "Dropping temporary siren_number index..."
psql -d postgres -f /app/scripts/sql/drop-temp-siren-index.sql

echo "Recreating all indexes from backup file..."
psql -d postgres -f /app/scripts/sql/recreate-indexes-from-backup.sql

echo "Verifying indexes match original state..."
psql -d postgres -f /app/scripts/sql/verify-indexes.sql

echo "Exporting DISTINCT values for autocomplete tables..."
/app/scripts/export-and-load-autocomplete.sh

# Reload Postgres configuration
psql -d postgres -c "SELECT pg_reload_conf();"

# Final VACUUM and analyze
echo "Running final VACUUM and ANALYZE..."
psql -d postgres -c "VACUUM FULL;"
psql -d postgres -c "ANALYZE;"

# Stop Postgres
pg_ctl -D "$PGDATA" -m fast stop

# Clean temporary files
rm -rf "$PGDATA"/pg_wal/archive_status/* "$PGDATA"/pg_stat_tmp/* "$PGDATA"/pg_logical/snapshots/* "$PGDATA"/pg_snapshots/*

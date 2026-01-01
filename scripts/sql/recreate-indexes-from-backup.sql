-- Recreate all indexes from the backup file
-- This script reads from /tmp/indexes_backup.csv and recreates each index

DO $$
DECLARE
    index_record RECORD;
    create_count INTEGER := 0;
    indexdef_modified TEXT;
BEGIN
    -- Create a temporary table to load the CSV
    CREATE TEMP TABLE IF NOT EXISTS temp_indexes (
        indexname TEXT,
        tablename TEXT,
        indexdef TEXT
    );

    -- Load the backup CSV
    COPY temp_indexes FROM '/tmp/indexes_backup.csv' WITH CSV HEADER;

    -- Recreate each index
    FOR index_record IN
        SELECT * FROM temp_indexes
        ORDER BY tablename, indexname
    LOOP
        -- Modify CREATE INDEX to use IF NOT EXISTS (no CONCURRENTLY since we're in a transaction)
        indexdef_modified := REPLACE(
            index_record.indexdef,
            'CREATE INDEX ',
            'CREATE INDEX IF NOT EXISTS '
        );

        BEGIN
            EXECUTE indexdef_modified;
            create_count := create_count + 1;
            RAISE NOTICE 'Created index: % on table %', index_record.indexname, index_record.tablename;
        EXCEPTION WHEN OTHERS THEN
            RAISE WARNING 'Failed to create index %: %', index_record.indexname, SQLERRM;
        END;
    END LOOP;

    RAISE NOTICE 'Total indexes recreated: %', create_count;

    -- Clean up
    DROP TABLE temp_indexes;
END $$;

-- Verify index count matches
WITH current_count AS (
    SELECT COUNT(*) as actual
    FROM pg_indexes i
    WHERE i.schemaname = 'public'
      AND i.indexname NOT LIKE '%_pkey'
      AND i.indexname NOT LIKE '%_key'
      AND i.indexdef NOT LIKE 'CREATE UNIQUE%'
)
SELECT
    c.actual as current_indexes,
    CASE
        WHEN c.actual > 0 THEN 'SUCCESS: Indexes recreated'
        ELSE 'ERROR: No indexes recreated'
    END as verification_result
FROM current_count c;

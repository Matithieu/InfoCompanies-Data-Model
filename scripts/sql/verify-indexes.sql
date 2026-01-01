-- Verify that all indexes from backup have been recreated
-- Compares current indexes against /tmp/indexes_backup.csv

DO $$
DECLARE
    backup_count INTEGER;
    current_count INTEGER;
    missing_count INTEGER;
    extra_count INTEGER;
    rec RECORD;
BEGIN
    -- Create temp table for comparison
    CREATE TEMP TABLE IF NOT EXISTS temp_backup_indexes (
        indexname TEXT,
        tablename TEXT,
        indexdef TEXT
    );

    -- Load the backup CSV
    COPY temp_backup_indexes FROM '/tmp/indexes_backup.csv' WITH CSV HEADER;

    -- Count indexes in backup
    SELECT COUNT(*) INTO backup_count FROM temp_backup_indexes;

    -- Count current indexes
    SELECT COUNT(*) INTO current_count
    FROM pg_indexes i
    WHERE i.schemaname = 'public'
      AND i.indexname NOT LIKE '%_pkey'
      AND i.indexname NOT LIKE '%_key'
      AND i.indexdef NOT LIKE 'CREATE UNIQUE%';

    -- Count missing indexes (in backup but not in current)
    SELECT COUNT(*) INTO missing_count
    FROM temp_backup_indexes b
    WHERE NOT EXISTS (
        SELECT 1
        FROM pg_indexes i
        WHERE i.schemaname = 'public'
          AND i.indexname = b.indexname
    );

    -- Count extra indexes (in current but not in backup)
    SELECT COUNT(*) INTO extra_count
    FROM pg_indexes i
    WHERE i.schemaname = 'public'
      AND i.indexname NOT LIKE '%_pkey'
      AND i.indexname NOT LIKE '%_key'
      AND i.indexdef NOT LIKE 'CREATE UNIQUE%'
      AND NOT EXISTS (
          SELECT 1
          FROM temp_backup_indexes b
          WHERE b.indexname = i.indexname
      );

    -- Print verification results
    RAISE NOTICE '========================================';
    RAISE NOTICE 'INDEX VERIFICATION RESULTS';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Expected indexes (from backup): %', backup_count;
    RAISE NOTICE 'Current indexes: %', current_count;
    RAISE NOTICE 'Missing indexes: %', missing_count;
    RAISE NOTICE 'Extra indexes: %', extra_count;
    RAISE NOTICE '========================================';

    -- List missing indexes if any
    IF missing_count > 0 THEN
        RAISE WARNING 'Missing indexes:';
        FOR rec IN
            SELECT b.indexname, b.tablename
            FROM temp_backup_indexes b
            WHERE NOT EXISTS (
                SELECT 1
                FROM pg_indexes i
                WHERE i.schemaname = 'public'
                  AND i.indexname = b.indexname
            )
        LOOP
            RAISE WARNING '  - % on table %', rec.indexname, rec.tablename;
        END LOOP;
    END IF;

    -- List extra indexes if any
    IF extra_count > 0 THEN
        RAISE WARNING 'Extra indexes (not in backup):';
        FOR rec IN
            SELECT i.indexname, i.tablename
            FROM pg_indexes i
            WHERE i.schemaname = 'public'
              AND i.indexname NOT LIKE '%_pkey'
              AND i.indexname NOT LIKE '%_key'
              AND i.indexdef NOT LIKE 'CREATE UNIQUE%'
              AND NOT EXISTS (
                  SELECT 1
                  FROM temp_backup_indexes b
                  WHERE b.indexname = i.indexname
              )
        LOOP
            RAISE WARNING '  - % on table %', rec.indexname, rec.tablename;
        END LOOP;
    END IF;

    -- Final verification
    IF backup_count = current_count AND missing_count = 0 AND extra_count = 0 THEN
        RAISE NOTICE '✓ SUCCESS: All indexes recreated correctly!';
    ELSE
        RAISE EXCEPTION 'INDEX VERIFICATION FAILED: Expected %, got % (missing: %, extra: %)',
            backup_count, current_count, missing_count, extra_count;
    END IF;

    -- Clean up
    DROP TABLE temp_backup_indexes;
END $$;

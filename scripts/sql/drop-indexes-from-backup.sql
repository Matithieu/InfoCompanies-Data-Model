-- Drop all indexes that were exported to the backup file
-- This script drops only regular indexes, not those backing constraints

DO $$
DECLARE
    index_record RECORD;
    drop_count INTEGER := 0;
    skip_count INTEGER := 0;
BEGIN
    -- Drop each index that's not a primary key
    FOR index_record IN
        SELECT i.indexname, i.tablename
        FROM pg_indexes i
        WHERE i.schemaname = 'public'
          AND i.indexname NOT LIKE '%_pkey'
        ORDER BY i.tablename, i.indexname
    LOOP
        BEGIN
            -- Try to drop the index
            EXECUTE format('DROP INDEX IF EXISTS public.%I', index_record.indexname);
            drop_count := drop_count + 1;
            RAISE NOTICE 'Dropped index: % on table %', index_record.indexname, index_record.tablename;
        EXCEPTION
            WHEN dependent_objects_still_exist THEN
                -- Skip indexes that have dependencies (unique constraints, foreign keys, etc.)
                skip_count := skip_count + 1;
                RAISE NOTICE 'Skipped index: % on table % (has dependencies)', index_record.indexname, index_record.tablename;
        END;
    END LOOP;

    RAISE NOTICE 'Total indexes dropped: %', drop_count;
    RAISE NOTICE 'Total indexes skipped: %', skip_count;
END $$;

-- Verify all droppable indexes are gone
SELECT
    CASE
        WHEN COUNT(*) = 0 THEN 'SUCCESS: All droppable indexes dropped'
        ELSE 'WARNING: ' || COUNT(*) || ' droppable indexes still exist'
    END as verification_result
FROM pg_indexes i
WHERE i.schemaname = 'public'
  AND i.indexname NOT LIKE '%_pkey'
  AND i.indexname NOT LIKE '%_key'
  AND i.indexdef NOT LIKE 'CREATE UNIQUE%';

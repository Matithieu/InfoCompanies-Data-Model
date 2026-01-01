-- Export all non-primary-key, non-unique indexes to a file for later recreation
-- This ensures we can recreate the exact same indexes after bulk data loading

-- Create machine-readable CSV for recreation
\copy (SELECT i.indexname, i.tablename, i.indexdef FROM pg_indexes i WHERE i.schemaname = 'public' AND i.indexname NOT LIKE '%_pkey' AND i.indexname NOT LIKE '%_key' AND i.indexdef NOT LIKE 'CREATE UNIQUE%' ORDER BY i.tablename, i.indexname) TO '/tmp/indexes_backup.csv' WITH (FORMAT CSV, HEADER true);

-- Print summary
SELECT
    COUNT(*) as total_indexes,
    COUNT(DISTINCT i.tablename) as affected_tables
FROM pg_indexes i
WHERE i.schemaname = 'public'
  AND i.indexname NOT LIKE '%_pkey'
  AND i.indexname NOT LIKE '%_key'
  AND i.indexdef NOT LIKE 'CREATE UNIQUE%';

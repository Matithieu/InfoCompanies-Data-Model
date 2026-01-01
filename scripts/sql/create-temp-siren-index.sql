-- Create a temporary index on companies.siren_number to optimize the UPDATE operation
-- in load_scrapped_companies.py which joins on siren_number
-- This index is critical for UPDATE performance (converts O(n²) to O(n log n))

CREATE INDEX IF NOT EXISTS ix_companies_siren_number_temp
ON public.companies(siren_number);

-- Analyze the table after creating the index to update statistics
ANALYZE public.companies;

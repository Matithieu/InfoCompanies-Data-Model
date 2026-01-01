-- Drop the temporary siren_number index after the UPDATE operation completes
-- This index will be recreated as part of create-indexes.sql with the proper name

DROP INDEX IF EXISTS public.ix_companies_siren_number_temp;

CREATE OR REPLACE FUNCTION datadog.pg_stat_activity()
RETURNS SETOF pg_stat_activity
LANGUAGE SQL
SECURITY DEFINER
SET search_path = pg_catalog
AS $$
    SELECT * FROM pg_catalog.pg_stat_activity;
$$;

CREATE OR REPLACE FUNCTION datadog.pg_stat_statements()
RETURNS SETOF pg_stat_statements
LANGUAGE SQL
SECURITY DEFINER
SET search_path = pg_catalog, public
AS $$
    SELECT * FROM public.pg_stat_statements;
$$;

CREATE OR REPLACE FUNCTION datadog.explain_statement(
    l_query TEXT,
    OUT explain JSON
)
RETURNS JSON
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = pg_catalog
AS $$
BEGIN
    EXECUTE 'SET TRANSACTION READ ONLY';
    EXECUTE 'EXPLAIN (FORMAT JSON) ' || l_query INTO explain;
END;
$$;

GRANT EXECUTE ON FUNCTION datadog.pg_stat_activity() TO datadog;
GRANT EXECUTE ON FUNCTION datadog.pg_stat_statements() TO datadog;
GRANT EXECUTE ON FUNCTION datadog.explain_statement(TEXT) TO datadog;

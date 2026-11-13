CREATE ROLE datadog WITH LOGIN INHERIT;
GRANT pg_monitor TO datadog;
CREATE SCHEMA IF NOT EXISTS datadog;
GRANT USAGE ON SCHEMA datadog TO datadog;
GRANT USAGE ON SCHEMA public TO datadog;
GRANT SELECT ON pg_stat_database TO datadog;

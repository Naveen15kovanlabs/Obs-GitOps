# postgres_exporter with read-only monitoring user (pg_monitor role) – Learnings

## Concepts Learned

### PostgreSQL
- Understood PostgreSQL database architecture and its purpose.
- Learned databases, schemas, tables, and database users.
- Understood the purpose of the default `postgres` database.
- Learned database connections and transaction management.

### Docker and Docker Compose
- Deployed PostgreSQL and monitoring services using Docker Compose.
- Learned container networking and service communication.
- Understood persistent volumes.
- Practiced container management and log inspection.

### PostgreSQL Exporter
- Understood how PostgreSQL Exporter collects database statistics.
- Learned how database metrics are exposed in Prometheus format.
- Configured exporter database connectivity.
- Troubleshot database authentication failures.

### Prometheus
- Configured Prometheus scrape targets.
- Understood metric scraping and time-series storage.
- Learned how to verify target health.
- Practiced querying PostgreSQL metrics using PromQL.

### Grafana
- Configured Prometheus as a Grafana data source.
- Imported a custom PostgreSQL dashboard using JSON.
- Learned different visualization types.
- Created monitoring panels for database health and performance.

## Troubleshooting Experience

- Resolved PostgreSQL exporter authentication issues.
- Inspected Docker container logs.
- Verified container and service connectivity.
- Validated Prometheus target status.
- Checked Grafana data source connectivity.

## Important Commands

| Command | Purpose |
|---|---|
| `docker compose ps` | Check container status |
| `docker compose up -d` | Start services |
| `docker compose down` | Stop services |
| `docker compose logs` | View container logs |
| `docker compose restart` | Restart services |
| `docker volume ls` | List Docker volumes |

## Key Takeaways

- PostgreSQL is the database layer.
- PostgreSQL Exporter collects database metrics.
- Prometheus scrapes and stores metrics.
- Grafana visualizes monitoring data.
- Docker Compose simplifies multi-container deployment.
- Authentication and networking are essential for monitoring connectivity.

## Task Outcome

Gained hands-on experience configuring PostgreSQL monitoring, collecting database metrics, validating Prometheus targets, creating Grafana dashboards, and troubleshooting monitoring components on AWS EC2.
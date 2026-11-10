# Service Monitoring – PostgreSQL & Redis

## Overview

This task focuses on monitoring existing PostgreSQL and Redis services using Prometheus, Grafana, Loki, and Grafana Alloy.

The objective is to build production-style monitoring for service health, performance, resource usage, logs, dashboards, alerts, and incident drills.

## Technologies Used

- PostgreSQL
- Redis
- Docker & Docker Compose
- Prometheus
- Grafana
- PostgreSQL Exporter
- Redis Exporter
- Loki
- Grafana Alloy
- Alertmanager
- Slack

## Monitoring Scope

| Area | Description |
|---|---|
| Metrics | Collect PostgreSQL and Redis performance metrics |
| Logs | Centralize and search service logs using Loki |
| Dashboards | Visualize service health and performance in Grafana |
| Usage | Track database growth, connections, and Redis memory |
| Alerts | Configure and test service monitoring alerts |
| Incident Drills | Simulate failures and validate alert detection |

## PostgreSQL Monitoring

- Database availability
- Active connections
- Transactions and rollbacks
- Cache hit ratio
- Locks and deadlocks
- Database and table size
- Slow queries
- Long-running transactions

## Redis Monitoring

- Redis availability
- Memory usage and maxmemory
- Cache hit and miss ratio
- Evictions
- Connected clients
- Operations per second
- Keyspace statistics
- Slowlog and persistence status

## Monitoring Architecture

```text
PostgreSQL ──> PostgreSQL Exporter ──┐
                                     │
Redis ───────> Redis Exporter ───────┤
                                     v
                                 Prometheus
                                     |
                                     v
                                  Grafana

PostgreSQL Logs ──┐
                  ├──> Grafana Alloy ──> Loki ──> Grafana
Redis Logs ───────┘

Prometheus ──> Alertmanager ──> Slack
```

## Task Plan

| Week | Focus |
|---|---|
| Week 2 | Metrics collection and log monitoring |
| Week 3 | Dashboards, usage monitoring, alerts, and incident drills |

## Repository Structure

```text
service monitoring/
│
├── README.md
│
├── postgres_exporter with read-only monitoring user (pg_monitor role)/
│   ├── compose.yaml
│   ├── prometheus.yml
│   ├── README.md
│   ├── learnings.md
│   ├── grafana/
│   └── images/
│
└── redis_exporter/
    └── (monitoring configuration and documentation)
```

## Expected Outcome

- Centralized PostgreSQL and Redis metrics.
- Searchable service logs.
- Grafana dashboards for monitoring and usage.
- Alerting integrated with Slack.
- Tested incident detection through failure simulations.
- Documentation and configuration maintained in Git.

## References

- [PostgreSQL Monitoring](https://www.postgresql.org/docs/current/monitoring-stats.html)
- [PostgreSQL Exporter](https://github.com/prometheus-community/postgres_exporter)
- [Redis INFO](https://redis.io/docs/latest/commands/info/)
- [Redis Exporter](https://github.com/oliver006/redis_exporter)
- [Prometheus](https://prometheus.io/docs/introduction/overview/)
- [Grafana](https://grafana.com/docs/)
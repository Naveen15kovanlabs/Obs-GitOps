# T1.6 - Nginx Log-Based Monitoring and Alerting

## Architecture

Nginx -> JSON access logs -> Grafana Alloy -> Loki -> Grafana

## Components

- Nginx: HTTP test application and JSON access logs.
- Grafana Alloy: Collects Nginx access logs and forwards them to Loki.
- Loki: Log storage and LogQL query engine.
- Grafana: Dashboard and alert rule evaluation.

## Endpoints

- /ok returns HTTP 200.
- /not-found returns HTTP 404.
- /server-error returns HTTP 500.
- /health returns HTTP 200.

## Dashboard

T1.6 | Nginx Log Monitoring & Incident Alerts

## Alerts

1. HTTP 5xx error rate greater than 5% over five minutes.
2. HTTP 404 count greater than 10 in one minute.

The 404 threshold is an assumed test threshold because the task does not specify one.

## Start

Copy .env.example to .env and configure a strong Grafana password.

Run:

docker compose up -d

## Verify

docker compose ps
docker compose logs --tail 30 alloy
docker compose logs --tail 30 loki
docker compose logs --tail 30 grafana

## Generate test traffic

Invoke /ok, /not-found and /server-error to generate HTTP 200, 404 and 500 logs.

## Security

Grafana is bound to 127.0.0.1:3000. Use AWS Systems Manager port forwarding.
Do not expose Grafana publicly.
Keep .env out of Git.

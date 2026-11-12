# T2.2 - RED Dashboard with P50/P95/P99

## Overview

Implemented application-level observability for a FastAPI application using Prometheus and Grafana.

The dashboard follows the RED methodology:

- **Rate:** HTTP requests per second.
- **Errors:** HTTP 5xx error rate and status-code distribution.
- **Duration:** P50, P95 and P99 request latency.

## Architecture

FastAPI Application -> Prometheus -> Grafana

- FastAPI exposes application metrics at `/metrics/`.
- Prometheus scrapes FastAPI metrics every 15 seconds.
- Grafana uses Prometheus as its data source.
- A provisioned RED dashboard displays application metrics.

## Project Structure

```text
.
├── app/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── prometheus/
│   └── prometheus.yml
├── grafana/
│   ├── provisioning/
│   │   ├── datasources/
│   │   │   └── prometheus.yml
│   │   └── dashboards/
│   │       └── dashboard.yml
│   └── dashboards/
│       └── red-dashboard.json
├── screenshots/
├── .env.example
├── .gitignore
├── compose.yaml
├── README.md
└── learnings.md
```

## Metrics Implemented

| Metric | Purpose |
|---|---|
| `http_requests_total` | Total HTTP requests |
| `http_request_duration_seconds` | Request duration histogram |
| `up{job="fastapi"}` | Application scrape availability |

## PromQL Functions

- `rate()` - Average per-second increase over a time window.
- `irate()` - Instantaneous rate using the latest two samples.
- `increase()` - Total counter increase over a time range.
- `histogram_quantile()` - Calculates latency percentiles from histogram buckets.

## Dashboard Panels

1. Request Rate
2. 5XX Error Rate
3. P95 Response Latency
4. Total Requests
5. Application Availability
6. Instantaneous Request Rate
7. Request Traffic by HTTP Method
8. P50/P95/P99 Latency Percentiles
9. Server Error Trend
10. Request Rate by Endpoint
11. HTTP Status Code Distribution
12. Endpoint Request Summary

## Run the Project

Create your local environment file:

```powershell
Copy-Item .env.example .env
notepad .env
```

Set a strong Grafana password in `.env`, then start services:

```bash
docker compose up -d --build
```

Check containers:

```bash
docker compose ps
```

## Local Access

- FastAPI: http://localhost:8000
- FastAPI Metrics: http://localhost:8000/metrics/
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

Grafana username: `admin`

Password: the value configured in `.env`.

The Compose file binds ports to localhost by default. For remote EC2 access, configure access deliberately and restrict the Security Group to trusted source IPs.

## Generate Test Traffic

```bash
for i in $(seq 1 30); do
  curl -s http://localhost:8000/ > /dev/null
  curl -s http://localhost:8000/items > /dev/null
  curl -s "http://localhost:8000/work?delay_ms=200" > /dev/null
done

for i in $(seq 1 10); do
  curl -s http://localhost:8000/error > /dev/null
done
```

Wait for Prometheus to scrape metrics, then refresh Grafana.

## Verification

- Verify the FastAPI Prometheus target is UP.
- Confirm request rate and total request panels show values.
- Confirm error panels show HTTP 500 test traffic.
- Confirm P50, P95 and P99 latency panels display data.
- Save screenshots in the `screenshots/` folder.

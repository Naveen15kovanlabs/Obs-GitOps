# T2.1 – Application Instrumentation: Request Counter, Latency Histogram, In-flight Gauge

## Overview

Implemented application-level monitoring for a Python FastAPI application using the Prometheus client library.

Instrumented the application with three Prometheus metric types: Counter, Histogram and Gauge. Configured Prometheus to scrape application metrics and integrated Grafana to visualize request activity and application performance.

## Architecture

```text
             HTTP Requests
                   |
                   v
          +------------------+
          |   FastAPI App    |
          |    Port 8000     |
          +------------------+
                   |
                   v
          +------------------+
          |  Instrumentation |
          |                  |
          |  Counter         |
          |  Histogram       |
          |  Gauge           |
          +------------------+
                   |
                   v
             /metrics/
                   |
                   v
          +------------------+
          |   Prometheus     |
          |    Port 9090     |
          +------------------+
                   |
                   v
          +------------------+
          |     Grafana      |
          |    Port 3000     |
          +------------------+
                   |
                   v
             Monitoring
             Dashboard
```

## Technologies Used

- AWS EC2 – Application hosting
- AWS Systems Manager (SSM) – Remote instance access
- Python – Application development
- FastAPI – REST API framework
- Prometheus Client – Application instrumentation
- Prometheus – Metrics collection and storage
- Grafana – Metrics visualization
- Linux – Server environment

## Application Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Application health check |
| GET | `/users` | Retrieve users |
| POST | `/users` | Create a user |
| GET | `/slow` | Simulate a slow request for Gauge testing |
| GET | `/metrics/` | Expose Prometheus metrics |

## Implemented Metrics

### 1. HTTP Request Counter

Metric: `http_requests_total`

Tracks the total number of HTTP requests processed by the application.

Labels:
- `method`
- `endpoint`
- `status`

### 2. Request Latency Histogram

Metric: `http_request_duration_seconds`

Measures the time taken to process HTTP requests.

Provides:
- Request duration sum
- Request duration count
- Duration buckets
- Percentile estimation using histogram buckets

### 3. In-flight Requests Gauge

Metric: `http_requests_in_flight`

Tracks the number of HTTP requests currently being processed.

The Gauge increases when a request starts and decreases when processing finishes.

## Prometheus Configuration

Prometheus scrapes the FastAPI application's `/metrics/` endpoint every 15 seconds.

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: "fastapi-app"
    metrics_path: /metrics/
    static_configs:
      - targets: ["localhost:8000"]
```

## Grafana Dashboard

Created a Grafana dashboard named **FastAPI Application Monitoring**.

Dashboard panels:

1. HTTP Request Rate
2. Total HTTP Requests
3. Average Request Latency
4. Requests In Flight
5. 95th Percentile Request Latency

## Testing and Validation

- Verified FastAPI endpoints using curl.
- Generated HTTP test traffic using shell loops.
- Verified Counter, Histogram and Gauge metrics through `/metrics/`.
- Confirmed Prometheus target status as `UP`.
- Queried application metrics through the Prometheus API.
- Tested the in-flight Gauge using the `/slow` endpoint.
- Verified application metrics through the Grafana dashboard.

## Project Structure

```text
T2.1 Instrument app request counter, latency histogram, in-flight gauge/
│
├── app/
│   ├── __init__.py
│   └── main.py
│
├── grafana/
│   └── fastapi-dashboard.json
│
├── screenshots/
├── requirements.txt
├── prometheus.yml
├── .gitignore
├── readme.md
└── learnings.md
```

## Outcome

Successfully implemented application instrumentation using Prometheus Counter, Histogram and Gauge metrics. Configured Prometheus for metrics collection and Grafana for visualization, enabling monitoring of HTTP request volume, request latency and active requests.
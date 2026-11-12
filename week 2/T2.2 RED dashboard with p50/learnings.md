# Learnings - T2.2 RED Dashboard

- Implemented application-level monitoring in FastAPI using Prometheus.
- Instrumented HTTP requests with a Counter and request duration with a Histogram.
- Configured Prometheus to scrape application metrics every 15 seconds.
- Integrated Grafana with Prometheus as the data source.
- Created a single RED dashboard covering request rate, errors and latency.
- Used rate(), irate() and increase() to analyse request traffic.
- Used histogram_quantile() to calculate P50, P95 and P99 latency.
- Analysed HTTP status codes and endpoint-level request traffic.
- Generated normal traffic and HTTP 500 errors to validate the dashboard.
- Practised verifying Prometheus targets and Grafana panels.

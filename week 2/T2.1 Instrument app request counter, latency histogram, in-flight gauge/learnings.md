# Learnings – T2.1 Application Instrumentation

## 1. Application Instrumentation

Learned how to instrument a FastAPI application to expose application-level metrics.

Instrumentation helps monitor application behaviour, request activity and performance without relying only on infrastructure-level monitoring.

## 2. Prometheus Metric Types

### Counter

- Learned how Counter metrics track cumulative events.
- Implemented `http_requests_total` to count incoming HTTP requests.
- Used labels such as HTTP method, endpoint and response status.

### Histogram

- Learned how Histogram metrics measure and record observations such as request processing time.
- Implemented `http_request_duration_seconds`.
- Understood histogram buckets, sum and count.
- Learned how histogram data can be used to estimate latency percentiles such as P95.

### Gauge

- Learned how Gauge metrics track values that can increase and decrease.
- Implemented `http_requests_in_flight` to monitor currently active HTTP requests.
- Used increment and decrement operations to track request lifecycle.

## 3. FastAPI Middleware

- Learned how FastAPI middleware intercepts incoming HTTP requests.
- Implemented middleware to measure request duration and update metrics.
- Used `time.perf_counter()` to measure request processing time.
- Used `try/finally` to ensure the Gauge is decremented even when request processing fails.
- Excluded the `/metrics/` endpoint from application request instrumentation to avoid counting Prometheus scrape traffic.

## 4. Prometheus Integration

- Learned how the Prometheus Python client exposes metrics through an HTTP endpoint.
- Configured Prometheus to scrape FastAPI metrics every 15 seconds.
- Understood scrape intervals, scrape targets and job names.
- Verified target health and queried application metrics using the Prometheus API.

## 5. Grafana Integration

- Learned how to connect Prometheus as a Grafana data source.
- Created a dashboard to visualize application metrics.
- Used PromQL queries for request rate, total requests, average latency, active requests and P95 latency.
- Understood how Grafana dashboards help identify application performance trends.

## 6. Testing and Validation

- Used curl to test FastAPI endpoints.
- Generated test traffic using shell loops.
- Verified metric values through the application metrics endpoint.
- Used Prometheus API queries to validate collected metrics.
- Tested the in-flight Gauge using a temporary slow endpoint.
- Observed that the Gauge returns to zero when the application becomes idle.

## 7. Key Takeaways

- Application instrumentation provides visibility into application-level performance.
- Counter tracks cumulative request counts.
- Histogram records request duration distributions.
- Gauge tracks values that change over time.
- Prometheus collects and stores application metrics.
- Grafana visualizes metrics through dashboards.
- Middleware provides a centralized way to instrument HTTP requests.

## Conclusion

Gained practical experience implementing application-level observability using FastAPI, Prometheus and Grafana. Understood how to instrument an application, expose metrics, collect time-series data and visualize application performance through a monitoring dashboard.
# T2.2 – RED Dashboard with P50 / P95 / P99

## What I Learned

- Learned how to add Prometheus metrics to a FastAPI application.
- Understood how Counter and Histogram metrics work.
- Learned how Prometheus collects application metrics through the `/metrics/` endpoint.
- Understood how to configure Prometheus scrape targets.
- Practiced writing PromQL queries using `rate()` and `sum()`.
- Learned how to calculate P50, P95, and P99 latency using `histogram_quantile()`.
- Understood why the `le` label is important when working with histogram buckets.
- Learned how to monitor request rates, HTTP errors, and response times.
- Created one Grafana dashboard with all the important RED metrics.
- Practiced generating normal requests, delayed requests, and HTTP 500 errors to test the dashboard.
- Learned how Docker Compose helps run the application and monitoring services together.

## Pros

- Can monitor application performance from a single Grafana dashboard.
- Easy to identify increases in request traffic and HTTP errors.
- P50, P95, and P99 help understand normal and slower response times.
- Prometheus and Grafana work well together for application monitoring.
- Docker Compose makes it easier to manage all the services in one place.
- The dashboard helps identify performance issues without checking application logs manually.

## Cons

- Histogram metrics need proper bucket configuration to get useful latency results.
- P95 and P99 values can change when the request volume is low.
- Prometheus stores time-series data, so storage and retention need to be managed.
- Too many dashboard panels can make monitoring difficult if they are not organized properly.
- If Prometheus cannot scrape the application, the Grafana dashboard may show missing data.
- More advanced monitoring may require additional metrics and alerting rules.

## My Overall Experience

This task helped me understand how application monitoring works in a practical environment. Initially, I focused on collecting request metrics, but later I understood how useful latency percentiles are for identifying slow requests.

The most interesting part for me was using `histogram_quantile()` to calculate P50, P95, and P99 and displaying all three in Grafana.

I also got practical experience with Docker Compose, Prometheus configuration, PromQL queries, and Grafana dashboard creation.

Overall, I got a better understanding of how to monitor an application using the RED methodology.
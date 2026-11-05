
#  Log Observability Dashboard

[dashboard]!(https://github.com/Naveen15kovanlabs/Obs-GitOps/blob/9a6014046bcbd5aa22887614292737b5101d8a42/week%201/T1.5/images/Screenshot%20(739).png)

## Overview

This task sets up centralized Nginx access-log monitoring for three Nginx servers using Grafana Alloy, Loki, and Grafana. Alloy collects the access logs from each server and forwards them to Loki. Grafana queries Loki to display request activity and HTTP response status codes in a dashboard.

## Architecture

```text
Nginx Server 1 ── Grafana Alloy ──┐
Nginx Server 2 ── Grafana Alloy ──┼──> Loki ──> Grafana Dashboard
Nginx Server 3 ── Grafana Alloy ──┘
```

## Dashboard Panels

- **Nginx Requests per Minute** — shows access-log request volume over time.
- **HTTP 404 Responses per Minute** — counts requests returning 404 responses.
- **HTTP 5xx Responses per Minute** — counts server-error responses.
- **Top 10 Requested Paths** — displays the most frequently requested paths over the last five minutes.
- **Recent Nginx Access Logs** — displays recent access-log entries from the three servers.

## Log Collection

Grafana Alloy runs on each Nginx server and collects its access logs. Each server’s logs are labeled with a `server` value so the dashboard can filter and compare traffic by server.

## Validation

1. Sent HTTP requests to the Nginx servers.
2. Verified that the access logs reached Loki.
3. Queried the logs in Grafana Explore.
4. Confirmed that the dashboard panels displayed request activity and response codes.

## Tools Used

- **Nginx** — web server generating access logs.
- **Grafana Alloy** — collects and forwards logs.
- **Loki** — stores and queries log data.
- **Grafana** — visualizes logs and metrics in the dashboard.
- **AWS EC2 and Systems Manager (SSM)** — host and access the private servers.

## Dashboard Configuration

The dashboard configuration is provided in `nginx-log-observability-dashboard.json`. Import the JSON into Grafana and select the Loki data source that receives the Nginx logs.

> The dashboard queries expect the `server` label values `nginx-1`, `nginx-2`, and `nginx-3`. Update the queries if your Alloy configuration uses different label values.

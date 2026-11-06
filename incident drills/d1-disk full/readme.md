# D1 – Disk Full Incident Drill

## 1. Overview

This document covers the implementation and execution of a Disk Full Incident Drill using Prometheus, Node Exporter, and Grafana on an AWS EC2 Ubuntu instance.

The objective was to simulate a real-world disk-space exhaustion scenario, monitor filesystem utilization, detect abnormal disk usage, evaluate predictive alerts, and understand the incident recovery process.

A dedicated test filesystem was used to safely simulate disk exhaustion without intentionally filling the EC2 root filesystem.

## 2. Objectives

- Configure a monitoring environment using Docker Compose.
- Deploy Prometheus, Node Exporter, and Grafana.
- Monitor Linux filesystem metrics.
- Configure Prometheus alerting rules.
- Create a Grafana disk monitoring dashboard.
- Simulate disk-space exhaustion.
- Observe threshold-based and predictive alerts.
- Validate incident detection.
- Perform disk cleanup and recovery.

## 3. Infrastructure and Tools

| Component | Configuration |
|---|---|
| Cloud Platform | AWS |
| Compute | Amazon EC2 |
| Operating System | Ubuntu Server |
| Instance Access | AWS Systems Manager (SSM) |
| Container Runtime | Docker |
| Container Management | Docker Compose |
| Metrics Collection | Node Exporter |
| Metrics Monitoring | Prometheus |
| Visualization | Grafana |
| Query Language | PromQL |
| Filesystem | ext4 |
| Test Filesystem | 2 GB loopback filesystem |

### Container Images

| Service | Image |
|---|---|
| Prometheus | prom/prometheus:v3.5.0 |
| Node Exporter | prom/node-exporter:v1.9.1 |
| Grafana | grafana/grafana:12.1.0 |

## 4. Monitoring Architecture

```text
             AWS EC2 - Ubuntu
                    |
                    |
          Dedicated Test Filesystem
              /mnt/diskdrill
                    |
                    v
              Node Exporter
               Port 9100
                    |
              Filesystem Metrics
                    |
                    v
                Prometheus
                Port 9090
                    |
             PromQL Alert Rules
                    |
                    v
                 Grafana
                Port 3000
                    |
                    v
            Monitoring Dashboard
```

### Component Responsibilities

**Node Exporter**

Collects Linux system and filesystem metrics, including:

- Total filesystem capacity.
- Available disk space.
- Free disk space.
- Filesystem utilization.
- Mountpoint information.

**Prometheus**

- Scrapes metrics from Node Exporter.
- Stores time-series metrics.
- Evaluates configured alerting rules.
- Supports PromQL queries.

**Grafana**

- Uses Prometheus as its data source.
- Visualizes disk utilization.
- Displays available and total disk capacity.
- Displays disk usage trends and alert states.

## 5. EC2 and Docker Setup

I created an Ubuntu EC2 instance and accessed it using AWS Systems Manager Session Manager.

Docker and Docker Compose were installed to deploy and manage the monitoring services.

### Directory Structure

```text
/opt/d1-disk-drill/
│
├── docker-compose.yml
├── .env
├── disk.img
│
├── prometheus/
│   ├── prometheus.yml
│   └── rules/
│       └── disk-alerts.yml
│
└── grafana/
    └── provisioning/
        └── datasources/
            └── prometheus.yml
```

### Docker Compose Services

The following services were deployed:

1. Prometheus
2. Node Exporter
3. Grafana

Persistent Docker volumes were configured for Prometheus and Grafana.

### Useful Commands

Check containers:

```bash
sudo docker compose ps
```

Start services:

```bash
sudo docker compose up -d
```

View logs:

```bash
sudo docker compose logs -f
```

Restart services:

```bash
sudo docker compose restart
```

## 6. Dedicated Disk Filesystem Configuration

To simulate disk exhaustion safely, I created a dedicated 2 GB loopback filesystem instead of filling the EC2 root filesystem.

Disk image:

```text
/opt/d1-disk-drill/disk.img
```

Mountpoint:

```text
/mnt/diskdrill
```

Filesystem:

```text
ext4
```

### Verify Filesystem

```bash
df -h /mnt/diskdrill
```

This filesystem is monitored separately through Node Exporter.

## 7. Prometheus Configuration

Prometheus was configured with two scrape targets.

| Job | Target |
|---|---|
| Prometheus | prometheus:9090 |
| Node Exporter | node-exporter:9100 |

File: `prometheus/prometheus.yml`

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - /etc/prometheus/rules/*.yml

scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets:
          - prometheus:9090

  - job_name: node-exporter
    static_configs:
      - targets:
          - node-exporter:9100
```

### Verify Prometheus

```bash
curl -s http://localhost:9090/-/ready
```

### Verify Scrape Targets

```bash
curl -s http://localhost:9090/api/v1/targets
```

Both Prometheus and Node Exporter targets were verified as `UP`.

## 8. Prometheus Alerting Rules

Two alerting rules were configured to monitor current disk utilization and predict possible filesystem exhaustion.

File: `prometheus/rules/disk-alerts.yml`

### 8.1 DiskUsageHigh

```yaml
groups:
  - name: disk-alerts
    rules:
      - alert: DiskUsageHigh
        expr: |
          100 * (
            1 -
            node_filesystem_avail_bytes{
              fstype="ext4",
              mountpoint="/mnt/diskdrill"
            }
            /
            node_filesystem_size_bytes{
              fstype="ext4",
              mountpoint="/mnt/diskdrill"
            }
          ) > 80
        for: 30s
        labels:
          severity: warning
        annotations:
          summary: Disk usage above 80%
          description: Disk usage on /mnt/diskdrill is above 80%.
```

**Explanation:**

- Calculates disk utilization percentage.
- Triggers when usage exceeds 80%.
- Requires the condition to remain true for 30 seconds.
- Uses warning severity.

### 8.2 DiskPredictedFull

```yaml
      - alert: DiskPredictedFull
        expr: |
          predict_linear(
            node_filesystem_avail_bytes{
              mountpoint="/mnt/diskdrill",
              fstype="ext4"
            }[5m],
            3600
          ) < 0
        for: 30s
        labels:
          severity: critical
        annotations:
          summary: Disk predicted to become full
          description: At the current rate, disk space may run out within one hour.
```

**Explanation:**

- Uses the `predict_linear()` PromQL function.
- Analyzes the previous five minutes of available disk-space metrics.
- Predicts available disk space 3,600 seconds into the future.
- Triggers when predicted available disk space becomes negative.
- Requires the condition to remain true for 30 seconds.

### Verify Alert Rules

```bash
curl -s http://localhost:9090/api/v1/rules
```

## 9. Grafana Dashboard Configuration

A dedicated Grafana dashboard was created using Prometheus as its data source.

**Dashboard:** D1 - Disk Full Incident Drill

**Refresh interval:** 15 seconds

### Dashboard Panels

| Panel | Visualization | Purpose |
|---|---|---|
| Disk Usage (%) | Gauge | Displays current disk utilization |
| Available Disk Space | Stat | Displays remaining storage |
| Total Disk Capacity | Stat | Displays total filesystem capacity |
| Disk Usage Trend | Time Series | Displays disk utilization over time |
| Disk Usage Alert (80%) | Stat | Displays threshold alert state |
| Predicted Disk Full Alert | Stat | Displays predictive alert state |

### Disk Usage Query

```promql
100 * (
  1 -
  node_filesystem_avail_bytes{
    mountpoint="/mnt/diskdrill",
    fstype="ext4"
  }
  /
  node_filesystem_size_bytes{
    mountpoint="/mnt/diskdrill",
    fstype="ext4"
  }
)
```

### Available Disk Space

```promql
node_filesystem_avail_bytes{
  mountpoint="/mnt/diskdrill",
  fstype="ext4"
}
```

### Total Disk Capacity

```promql
node_filesystem_size_bytes{
  mountpoint="/mnt/diskdrill",
  fstype="ext4"
}
```

### Disk Usage Alert

```promql
ALERTS{
  alertname="DiskUsageHigh",
  alertstate="firing"
}
```

### Predicted Disk Full Alert

```promql
ALERTS{
  alertname="DiskPredictedFull",
  alertstate="firing"
}
```

## 10. Incident Simulation – Disk Space Exhaustion

After configuring the monitoring environment and Grafana dashboard, I performed a controlled disk-full simulation.

### 10.1 Initial Filesystem State

Before injecting the incident, I checked the filesystem utilization.

```bash
df -h /mnt/diskdrill
```

The initial filesystem utilization was approximately 1%.

Prometheus was successfully collecting the filesystem metrics through Node Exporter.

### 10.2 Incident Injection

I gradually consumed disk space by writing data to a test file inside the dedicated filesystem.

Test file:

```text
/mnt/diskdrill/fill.test
```

Command used:

```bash
sudo bash -c '
FILE=/mnt/diskdrill/fill.test

echo "Incident started:"
date -Is

while true; do
  dd if=/dev/zero of="$FILE" bs=10M count=1 oflag=append conv=notrunc status=none

  USAGE=$(df -P /mnt/diskdrill | awk "NR==2 {gsub(\"%\",\"\",\$5); print \$5}")

  echo "Disk usage: ${USAGE}%"

  if [ "$USAGE" -ge 85 ]; then
    break
  fi

  sleep 1
done

echo "Incident injection completed:"
date -Is
'
```

The command:

1. Writes data in 10 MB increments.
2. Checks filesystem utilization after each write.
3. Continues until disk usage reaches at least 85%.
4. Stops automatically after reaching the threshold.

### 10.3 Observed Incident Results

During the simulation, the Grafana dashboard displayed:

| Metric | Observed Value |
|---|---:|
| Disk Usage | 85.3% |
| Available Disk Space | 286.93 MiB |
| Total Disk Capacity | 1.90 GiB |
| Predicted Disk Full Alert | FIRING |
| Disk Usage Alert (80%) | Normal in captured screenshot |

The disk usage trend showed a significant increase from the initial baseline to approximately 85%.

The predictive disk-full alert entered the firing state.

The DiskUsageHigh panel was still displaying Normal in the captured screenshot. Its final firing state needs to be verified after the 30-second pending period.

### 10.4 Alert Validation

To inspect the alert states:

```bash
curl -s http://localhost:9090/api/v1/alerts
```

To inspect configured alert rules:

```bash
curl -s http://localhost:9090/api/v1/rules
```

These endpoints help distinguish between configured rules, pending alerts, and firing alerts.

## 11. Incident Analysis

The simulation demonstrated how filesystem metrics can be used to identify disk-space exhaustion.

Observations:

1. Node Exporter successfully collected filesystem metrics.
2. Prometheus scraped the metrics at 15-second intervals.
3. Grafana visualized the increase in disk utilization.
4. Available disk space decreased as data was written.
5. The predictive alert detected the rapid decrease in available storage.
6. The dashboard provided visibility into the filesystem condition.

### Difference Between the Alerts

**DiskUsageHigh**

Detects an existing high disk-utilization condition when usage remains above 80%.

**DiskPredictedFull**

Predicts future disk exhaustion based on the recent rate of change in available disk space.

The predictive alert can fire independently of the threshold-based alert.

## 12. Incident Recovery

The following recovery procedure removes the injected test data and restores the filesystem.

### Step 1 – Check Current Disk Usage

```bash
df -h /mnt/diskdrill
```

### Step 2 – Remove Injected Test Data

```bash
sudo rm -f /mnt/diskdrill/fill.test
```

### Step 3 – Verify Available Storage

```bash
df -h /mnt/diskdrill
```

### Step 4 – Verify Alert Recovery

```bash
curl -s http://localhost:9090/api/v1/alerts
```

After the filesystem metrics are updated and the alert conditions are no longer true, the alerts should return to inactive.

### Recovery Checklist

- [ ] Injected test file removed.
- [ ] Disk usage returned to baseline.
- [ ] Available disk space restored.
- [ ] Prometheus metrics updated.
- [ ] DiskUsageHigh returned to inactive.
- [ ] DiskPredictedFull returned to inactive.

## 13. Alert Notification Status

The current configuration evaluates Prometheus alerting rules and displays their states in Grafana.

External notification delivery has not been configured.

Possible notification integrations include:

- Prometheus Alertmanager.
- Slack notifications.
- Email notifications.
- Grafana notification policies.

A firing alert in Prometheus or Grafana does not automatically mean that an external notification has been delivered.

## 14. Troubleshooting Commands

### Check Containers

```bash
sudo docker compose ps
```

### Prometheus Logs

```bash
sudo docker compose logs prometheus
```

### Node Exporter Logs

```bash
sudo docker compose logs node-exporter
```

### Grafana Logs

```bash
sudo docker compose logs grafana
```

### Check Disk Utilization

```bash
df -h /mnt/diskdrill
```

### Check Filesystem Metrics

```bash
curl -sG http://localhost:9090/api/v1/query \
  --data-urlencode 'query=node_filesystem_size_bytes{mountpoint="/mnt/diskdrill"}'
```

### Check Prometheus Targets

```bash
curl -s http://localhost:9090/api/v1/targets
```

### Check Alert Rules

```bash
curl -s http://localhost:9090/api/v1/rules
```

### Check Active Alerts

```bash
curl -s http://localhost:9090/api/v1/alerts
```

## 15. Key Learnings

Through this incident drill, I gained practical experience in:

- Deploying Prometheus, Node Exporter, and Grafana using Docker Compose.
- Configuring Prometheus scrape targets.
- Understanding Linux filesystem metrics.
- Monitoring disk utilization and available storage.
- Writing PromQL queries.
- Configuring Prometheus alerting rules.
- Understanding alert evaluation and pending durations.
- Using `predict_linear()` for predictive disk monitoring.
- Building Grafana dashboards using Gauge, Stat, and Time Series panels.
- Simulating disk-space exhaustion safely.
- Investigating alert states.
- Understanding incident recovery procedures.
- Differentiating alert evaluation from external notification delivery.

## 16. Further Enhancements

- Configure Prometheus Alertmanager.
- Integrate Slack and email notifications.
- Monitor filesystem inode utilization.
- Add CPU and memory monitoring.
- Extend monitoring to multiple EC2 instances.
- Automate cleanup and recovery procedures.
- Manage dashboards and monitoring configurations through GitOps.
- Provision the monitoring infrastructure using Terraform.

## 17. Summary

The D1 Disk Full Incident Drill covered the complete monitoring workflow, from filesystem metric collection and Prometheus alert evaluation to Grafana visualization and incident simulation.

A dedicated test filesystem was used to simulate disk exhaustion. Disk utilization reached approximately 85.3%, and the predictive disk-full alert entered the firing state.

This exercise provided practical experience in Linux monitoring, Prometheus alerting, PromQL, Grafana visualization, incident investigation, and disk-space recovery.
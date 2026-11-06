# D1 – Disk Full Incident Drill

## 1. Overview

This document covers a controlled Disk Full Incident Drill using Prometheus, Node Exporter and Grafana on an AWS EC2 Ubuntu instance.

The objective was to simulate disk-space exhaustion, monitor filesystem utilization, detect abnormal disk usage, evaluate predictive alerts and understand the recovery process.

To avoid intentionally filling the EC2 root filesystem, I used a dedicated 2 GB loopback filesystem mounted at `/mnt/diskdrill`.

## 2. Objectives

- Deploy Prometheus, Node Exporter and Grafana using Docker Compose.
- Monitor Linux filesystem metrics.
- Configure Prometheus alerting rules.
- Build a Grafana disk monitoring dashboard.
- Simulate disk-space exhaustion using a test file.
- Observe threshold-based and predictive alerts.
- Validate alert state transitions.
- Remove the test data and verify recovery.

## 3. Infrastructure and Tools

| Component | Configuration |
|---|---|
| Cloud Platform | AWS |
| Compute | Amazon EC2 |
| Operating System | Ubuntu Server |
| Instance Access | AWS Systems Manager Session Manager |
| Container Runtime | Docker |
| Container Management | Docker Compose |
| Metrics Collection | Node Exporter |
| Metrics Monitoring | Prometheus |
| Visualization | Grafana |
| Query Language | PromQL |
| Filesystem | ext4 |
| Test Filesystem | 2 GB loopback filesystem |
| Mountpoint | `/mnt/diskdrill` |

### Container Images

| Service | Image |
|---|---|
| Prometheus | `prom/prometheus:v3.5.0` |
| Node Exporter | `prom/node-exporter:v1.9.1` |
| Grafana | `grafana/grafana:12.1.0` |

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
                 Disk Monitoring Dashboard
```

### Component Responsibilities

**Node Exporter**
- Collects Linux system and filesystem metrics.
- Exposes filesystem capacity and available-space metrics.
- Provides mountpoint and filesystem information.

**Prometheus**
- Scrapes metrics from Node Exporter.
- Stores time-series data.
- Evaluates configured alerting rules.
- Supports PromQL queries.

**Grafana**
- Uses Prometheus as its data source.
- Displays disk utilization and available storage.
- Visualizes disk usage trends.
- Displays the alert states.

## 5. EC2 and Docker Setup

I created an Ubuntu EC2 instance and accessed it using AWS Systems Manager Session Manager.

Docker and Docker Compose were installed to deploy and manage the monitoring services.

The monitoring stack was started using:

```bash
sudo docker compose up -d
```

I verified the running containers using:

```bash
sudo docker compose ps
```

The three services started successfully:

1. Prometheus
2. Node Exporter
3. Grafana

### Deployment Verification

The first screenshot shows the container images being pulled, Docker volumes being created, the containers starting and the test filesystem being mounted.

![Monitoring stack deployment and filesystem setup](images/Screenshot%20%28740%29.png)

*Figure 1 – Docker Compose deployment and initial filesystem setup.*

### Directory Structure on EC2

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

Persistent Docker volumes were configured for Prometheus and Grafana.

### Useful Docker Commands

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

I created a dedicated 2 GB loopback filesystem to safely simulate disk exhaustion.

| Property | Value |
|---|---|
| Disk image | `/opt/d1-disk-drill/disk.img` |
| Mountpoint | `/mnt/diskdrill` |
| Filesystem | ext4 |
| Approximate capacity | 1.90 GiB usable |

The filesystem was mounted separately so that the incident simulation would target the test filesystem rather than intentionally filling the EC2 root filesystem.

### Verify Filesystem

```bash
df -h /mnt/diskdrill
```

Node Exporter was configured to collect metrics for this mountpoint.

## 7. Prometheus Configuration

Prometheus was configured with two scrape targets.

| Job | Target |
|---|---|
| Prometheus | `prometheus:9090` |
| Node Exporter | `node-exporter:9100` |

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

I configured two alerting rules to monitor current disk utilization and predict possible filesystem exhaustion.

File: `prometheus/rules/disk-alerts.yml`

### 8.1 DiskUsageHigh

```yaml
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

**How it works:**

- Calculates filesystem utilization as a percentage.
- Triggers when disk usage exceeds 80%.
- Waits for the condition to remain true for 30 seconds.
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

**How it works:**

- Uses the `predict_linear()` PromQL function.
- Analyses the previous five minutes of available disk-space metrics.
- Estimates available disk space 3,600 seconds into the future.
- Triggers if the projected available space becomes negative.
- Waits for the condition to remain true for 30 seconds.

### Verify Alert Rules

```bash
curl -s http://localhost:9090/api/v1/rules
```

## 9. Grafana Dashboard

I created a dedicated Grafana dashboard using Prometheus as its data source.

**Dashboard:** D1 - Disk Full Incident Drill

**Refresh interval:** 15 seconds

### Dashboard Panels

| Panel | Visualization | Purpose |
|---|---|---|
| Disk Usage (%) | Gauge | Current filesystem utilization |
| Available Disk Space | Stat | Remaining disk space |
| Total Disk Capacity | Stat | Total filesystem capacity |
| Disk Usage Trend | Time Series | Disk utilization over time |
| Disk Usage Alert (80%) | Stat | Threshold alert state |
| Predicted Disk Full Alert | Stat | Predictive alert state |

### Dashboard Queries

**Disk Usage (%)**

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

**Available Disk Space**

```promql
node_filesystem_avail_bytes{
  mountpoint="/mnt/diskdrill",
  fstype="ext4"
}
```

**Total Disk Capacity**

```promql
node_filesystem_size_bytes{
  mountpoint="/mnt/diskdrill",
  fstype="ext4"
}
```

**Disk Usage Alert**

```promql
ALERTS{
  alertname="DiskUsageHigh",
  alertstate="firing"
}
```

**Predicted Disk Full Alert**

```promql
ALERTS{
  alertname="DiskPredictedFull",
  alertstate="firing"
}
```

## 10. Incident Simulation – Disk Space Exhaustion

After deploying the monitoring stack and creating the dashboard, I performed a controlled disk-full simulation.

### 10.1 Initial Dashboard State

Before injecting the incident, I checked the dashboard to confirm that filesystem metrics were being collected.

The initial dashboard screenshot showed:

| Metric | Observed Value |
|---|---:|
| Disk Usage | 6.11% |
| Available Disk Space | 1.78 GiB |
| Total Disk Capacity | 1.90 GiB |
| Disk Usage Alert | Normal |
| Predicted Disk Full Alert | Normal |

Both alert panels were Normal, indicating that neither alert was firing at that point.

![Initial Grafana dashboard](images/Screenshot%20%28741%29.png)

*Figure 2 – Initial disk monitoring dashboard before the incident.*

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

The terminal screenshot shows disk usage gradually increasing during the simulation.

![Disk usage increasing during incident injection](images/Screenshot%20%28742%29.png)

*Figure 3 – Terminal output showing the gradual increase in filesystem utilization.*

### 10.3 Predictive Alert Detection

As disk usage increased, the Grafana dashboard showed the following state:

| Metric | Observed Value |
|---|---:|
| Disk Usage | 41.1% |
| Available Disk Space | 1.12 GiB |
| Total Disk Capacity | 1.90 GiB |
| Predicted Disk Full Alert | FIRING |
| Disk Usage Alert (80%) | Normal |

The `DiskPredictedFull` alert entered the firing state before disk utilization reached 80%.

This happened because `predict_linear()` estimated that available disk space could become negative within the configured prediction window if the current rate of disk consumption continued.

![Predictive alert firing at 41.1 percent disk usage](images/Screenshot%20%28743%29.png)

*Figure 4 – Predictive disk-full alert firing while the threshold alert remains Normal.*

### 10.4 Disk Utilization Reaches 85.3%

The simulation continued until filesystem utilization reached approximately 85.3%.

The dashboard displayed:

| Metric | Observed Value |
|---|---:|
| Disk Usage | 85.3% |
| Available Disk Space | 286.93 MiB |
| Total Disk Capacity | 1.90 GiB |
| Predicted Disk Full Alert | FIRING |
| Disk Usage Alert (80%) | Normal |

At this point, the predictive alert was still firing. The threshold alert was still displaying Normal in this screenshot because its 30-second pending period had not yet completed.

![Disk usage reaches 85.3 percent](images/Screenshot%20%28744%29.png)

*Figure 5 – Disk utilization reaches 85.3%, while the threshold alert is still pending.*

### 10.5 Threshold Alert Detection

After the disk usage remained above 80% for the configured 30-second duration, the `DiskUsageHigh` alert also entered the firing state.

The dashboard showed:

| Metric | Observed Value |
|---|---:|
| Disk Usage | 85.3% |
| Available Disk Space | 286.93 MiB |
| Total Disk Capacity | 1.90 GiB |
| Predicted Disk Full Alert | FIRING |
| Disk Usage Alert (80%) | FIRING |

Both alerts were now firing.

![Both disk alerts firing at 85.3 percent usage](images/Screenshot%20%28745%29.png)

*Figure 6 – Both predictive and threshold-based alerts are firing.*

## 11. Incident Analysis

The screenshots demonstrate how the two alerting rules detect different stages of a disk-space incident.

### Alert State Progression

| Stage | Disk Usage | Predicted Alert | Threshold Alert |
|---|---:|---|---|
| Initial dashboard | 6.11% | Normal | Normal |
| Predictive detection | 41.1% | Firing | Normal |
| High utilization | 85.3% | Firing | Normal |
| After pending duration | 85.3% | Firing | Firing |

### Difference Between the Alerts

**DiskPredictedFull**

- Uses historical available-space metrics.
- Estimates future disk availability.
- Can detect potential exhaustion before the disk reaches a high utilization threshold.

**DiskUsageHigh**

- Detects an existing high disk-utilization condition.
- Triggers when usage exceeds 80%.
- Requires the condition to remain true for 30 seconds.

The simulation demonstrated that a predictive alert can fire before a threshold-based alert.

## 12. Incident Recovery

After observing both alerts firing, the recovery procedure is to remove the injected test data and verify that filesystem capacity is restored.

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

After Prometheus collects updated filesystem metrics and the alert conditions are no longer true, the alerts should return to inactive.

### Recovery Checklist

- [ ] Injected test file removed.
- [ ] Disk usage returned to baseline.
- [ ] Available disk space restored.
- [ ] Prometheus metrics updated.
- [ ] `DiskUsageHigh` returned to inactive.
- [ ] `DiskPredictedFull` returned to inactive.

## 13. Alert Notification Status

The configured Prometheus alerting rules evaluate filesystem conditions and expose their alert states.

The Grafana dashboard displays these states, but external notification delivery has not been configured.

Possible future integrations include:

- Prometheus Alertmanager.
- Slack notifications.
- Email notifications.
- Grafana notification policies.

A firing alert in Prometheus or Grafana does not automatically mean that an external notification has been delivered.

## 14. Troubleshooting Commands

**Check running containers**

```bash
sudo docker compose ps
```

**Prometheus logs**

```bash
sudo docker compose logs prometheus
```

**Node Exporter logs**

```bash
sudo docker compose logs node-exporter
```

**Grafana logs**

```bash
sudo docker compose logs grafana
```

**Check disk utilization**

```bash
df -h /mnt/diskdrill
```

**Check filesystem metrics**

```bash
curl -sG http://localhost:9090/api/v1/query \
  --data-urlencode 'query=node_filesystem_size_bytes{mountpoint="/mnt/diskdrill"}'
```

**Check Prometheus targets**

```bash
curl -s http://localhost:9090/api/v1/targets
```

**Check alert rules**

```bash
curl -s http://localhost:9090/api/v1/rules
```

**Check active alerts**

```bash
curl -s http://localhost:9090/api/v1/alerts
```

## 15. Key Learnings

Through this incident drill, I gained practical experience in:

- Deploying Prometheus, Node Exporter and Grafana using Docker Compose.
- Configuring Prometheus scrape targets.
- Understanding Linux filesystem metrics.
- Monitoring disk utilization and available storage.
- Writing PromQL queries.
- Configuring Prometheus alerting rules.
- Understanding alert evaluation and pending durations.
- Using `predict_linear()` for predictive disk monitoring.
- Building Grafana dashboards using Gauge, Stat and Time Series panels.
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

The D1 Disk Full Incident Drill covered the monitoring workflow from filesystem metric collection and Prometheus alert evaluation to Grafana visualization and incident simulation.

A dedicated test filesystem was used to simulate disk-space exhaustion safely.

During the simulation:

- Disk utilization increased from its initial baseline to 85.3%.
- The predictive disk-full alert fired at approximately 41.1% utilization.
- The threshold-based alert fired after disk usage remained above 80% for 30 seconds.
- Both alerts were visible as FIRING in the final captured dashboard.

This exercise provided practical experience in Linux filesystem monitoring, Prometheus alerting, PromQL, Grafana visualization, incident investigation and disk-space recovery.

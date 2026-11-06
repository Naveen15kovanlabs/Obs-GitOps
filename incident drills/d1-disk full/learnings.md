# Learnings – D1 Disk Full Incident Drill

While working on this incident drill, I learned how disk monitoring works and how to identify disk space issues using Prometheus and Grafana.

### What I learned

- Set up Prometheus, Node Exporter, and Grafana using Docker Compose.
- Understood how Node Exporter collects disk and filesystem metrics from Linux.
- Learned how Prometheus collects and stores those metrics.
- Understood how scrape intervals work and why Prometheus needs to collect metrics regularly.
- Learned how to monitor disk usage, available space, and total disk capacity.
- Created PromQL queries to calculate disk usage percentage.
- Understood how alert rules work in Prometheus.
- Learned the difference between a normal disk usage alert and a predictive disk-full alert.
- Understood how `predict_linear()` helps estimate when disk space might run out.
- Created a Grafana dashboard using Gauge, Stat, and Time Series panels.
- Learned how to simulate a disk-full situation using a separate test filesystem instead of filling the main EC2 disk.
- Observed disk usage increase to around 85% during the test.
- Saw the predicted disk-full alert enter the firing state.
- Understood why an alert may take some time to fire because of the `for: 30s` condition.
- Learned how to check alert states using Prometheus API endpoints.
- Understood that displaying an alert in Grafana is different from sending an actual Slack or email notification.
- Learned how to remove the test file and restore available disk space.

### Things I understood better

- Node Exporter is responsible for collecting metrics, not visualizing them.
- Prometheus collects metrics, evaluates alert rules, and stores time-series data.
- Grafana uses Prometheus as a data source to visualize the collected metrics.
- A threshold alert tells us when disk usage is already high.
- A predictive alert helps identify possible disk exhaustion before the disk becomes completely full.
- Docker Compose makes it easier to manage multiple monitoring containers together.

### Overall Learning

This drill helped me understand how disk monitoring works in a practical environment. I got to see how disk usage changes in real time, how Prometheus evaluates alert conditions, and how Grafana helps us understand what is happening.

I also understood that monitoring is not just about collecting metrics. We need to identify the issue, verify the alert, investigate the cause, and recover the system properly.
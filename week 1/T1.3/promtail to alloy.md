# Migrate Promtail → Grafana Alloy

A logging stack that runs with Docker Compose on one EC2 instance.

- **Loki** stores the logs
- **Grafana** shows them
- **Alloy** collects system logs and Docker container logs and sends them to Loki

This repo is the result of migrating from **Promtail to Grafana Alloy** (task T1.3). Promtail is gone, and Alloy does its job now.

## Folder layout

```
docker-compose.yml                         Loki, Grafana and Alloy
loki/loki-config.yaml                      Loki settings (7 day retention)
alloy/config.alloy                         Alloy settings (what to collect, where to send)
grafana/provisioning/datasources/loki.yml  adds Loki to Grafana automatically
.env                                       secrets (NOT in Git, create it yourself)
```

## What you need

- An EC2 instance (Ubuntu) with Docker and the Compose plugin installed
- Your user in the `docker` group (log out and back in after adding it)
- Security group: TCP 3000 open to **your IP only**. Don't open Loki (3100) or Alloy (12345)

## Setup

1. Clone the repo and go into the folder.

2. Create a `.env` file. It is ignored by Git, so it never gets pushed:

```
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=pick-a-strong-password
HOST_LABEL=ec2-observability-01
LOKI_URL=http://loki:3100/loki/api/v1/push
```

3. Check the compose file, then start everything:

```
docker compose config > /dev/null && echo FILES-OK
docker compose up -d
docker compose ps
```

You should see `loki`, `grafana` and `alloy` as Up.

## Look at the logs in Grafana

1. Open `http://<EC2_PUBLIC_IP>:3000` and log in with the values from `.env`.
2. Go to **Explore** and pick the **Loki** data source.
3. Set the time range to **Last 15 minutes** and run:

```
{job="varlogs"}
```
System logs (syslog, auth.log and so on).

```
{job="docker"}
```
Logs from the Docker containers.

The labels are `job` and `host`.

## How the migration went

1. Started Loki, Grafana and Promtail, and checked the logs in Grafana.
2. Added Alloy next to Promtail. Both sent logs for a while, tagged with a temporary `collector` label (`promtail` or `alloy`), so I could compare them in Grafana.
3. Counts for the same job matched, so I stopped Promtail and removed it.
4. Merged Alloy into the main `docker-compose.yml` and removed the extra compose files.
5. Committed the Alloy config to GitHub.

Handy comparison query used during the migration:

```
sum by (collector, job) (count_over_time({collector=~"alloy|promtail"}[10m]))
```

## Useful commands

```
docker compose ps                 see what is running
docker logs alloy --tail 30       check Alloy for errors
docker compose stop alloy         stop one service
docker compose restart alloy      restart one service
docker compose up -d              start or update everything
```

## If something goes wrong

- **No logs in Grafana:** widen the time range, then run `docker logs alloy --tail 30`. If it says `connection refused`, wait about 15 seconds for Loki to finish starting.
- **`permission denied` on Docker:** your user isn't in the `docker` group yet. Add it, then open a new session. If you use Session Manager, the user is `ssm-user`.
- **Can't open Grafana:** check the security group rule for port 3000 and that your current IP hasn't changed.

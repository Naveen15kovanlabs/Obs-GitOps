# T1.3 - Observability stack

This folder contains a Docker Compose stack for Grafana, Loki, and a log
collector. Choose Alloy or Promtail; both collectors send logs to Loki.

## Configure

```bash
cp .env.example .env
```

Edit `.env` and set a strong `GRAFANA_ADMIN_PASSWORD` and an appropriate
`HOST_LABEL`. Keep `.env` private; it is ignored by Git.

## Start the stack

Start the base services and Alloy:

```bash
docker compose -f docker-compose.yml -f docker-compose.alloy.yml up -d
```

To use Promtail instead, start the base services and Promtail:

```bash
docker compose -f docker-compose.yml -f docker-compose.promtail.yml up -d
```

During a migration, both collectors can be started temporarily to compare
their logs. Avoid leaving both enabled after verification, since this can
produce duplicate log entries.

## Verify

- Grafana: http://localhost:3000
- Alloy UI (when using Alloy): http://localhost:12345
- In Grafana, open **Explore**, select **Loki**, and query `{job="varlogs"}` or
  `{job="docker"}`.

Check container output if logs are missing:

```bash
docker compose -f docker-compose.yml -f docker-compose.alloy.yml logs -f alloy
docker compose -f docker-compose.yml -f docker-compose.promtail.yml logs -f promtail
```

## Stop

Stop the selected stack without removing its persistent data:

```bash
docker compose -f docker-compose.yml -f docker-compose.alloy.yml down
```

Replace `docker-compose.alloy.yml` with `docker-compose.promtail.yml` when
stopping a Promtail stack. Do not add `-v` unless you intend to delete Loki,
Grafana, and collector data.

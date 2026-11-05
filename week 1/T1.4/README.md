# Nginx Log Monitoring: Alloy -> Loki -> Grafana

Three Nginx containers on separate AWS EC2 Ubuntu instances; Grafana Alloy on each ships logs to a central Loki; Grafana explores them with LogQL.

![Nginx Logs](images/nginx%20logs.png)

![Screenshot 733](images/Screenshot%20(733).png)

![Screenshot 734](images/Screenshot%20(734).png)

![Screenshot 735](images/Screenshot%20(735).png)

![Screenshot 736](images/Screenshot%20(736).png)

![Screenshot 737](images/Screenshot%20(737).png)

![Screenshot 2026-11-04 160110](images/Screenshot%202026-11-04%20160110.png)

![Screenshot 2026-11-04 160757](images/Screenshot%202026-11-04%20160757.png)

![Screenshot 2026-11-04 161024](images/Screenshot%202026-11-04%20161024.png)

## Structure

```
nginx-node/            # deploy on each Nginx EC2 instance
  docker-compose.yml
  alloy/config.alloy   # single shared config
  envs/nginx-{1,2,3}.env
observability-server/  # deploy on the central server
  docker-compose.yml
  .env.example
  loki/loki-config.yml
  grafana/provisioning/datasources/loki.yml
queries/nginx-logql.txt
scripts/               # generate-traffic.sh, verify.sh
docs/architecture.md
```

## 1. Central server (Loki + Grafana)

```bash
cd observability-server
cp .env.example .env     # set a real Grafana password
docker compose up -d
```

Grafana: `http://<SERVER_IP>:3000`

## 2. Each Nginx instance

```bash
cd nginx-node
docker compose --env-file envs/nginx-1.env up -d   # nginx-2.env / nginx-3.env on the others
```

Change `LOKI_URL` in `envs/*.env` if the Loki private IP is not `10.0.0.51`.

## 3. Verify

```bash
./scripts/generate-traffic.sh          # on a Nginx node
./scripts/verify.sh                    # on the Loki server
```

In Grafana > Explore > Loki:

```
{server=~"nginx-1|nginx-2|nginx-3"} |= "HTTP/"
```

## Security groups

- TCP 3100: Nginx instances -> Loki server
- TCP 3000: your IP -> Grafana
- TCP 80: your IP -> Nginx instances (testing)

Alloy mounts the Docker socket; keep hosts locked down.

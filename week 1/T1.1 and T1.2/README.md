# T1.1 - Nginx + Flask app with a scheduled k6 load generator

## What I implemented

I built a small Flask API and placed Nginx in front of it as a reverse proxy.
I also added a static endpoint-testing page so I can test the API from a
browser instead of reading raw JSON responses.

I added a k6 load-test script in `k6/load-test.js`. The script sends requests
through Nginx at `http://host.docker.internal:8080/`, uses 5 virtual users,
runs for 1 minute, and waits 1 second between requests. This gives me
repeatable traffic that I can use to check the Nginx access logs.

I run the k6 command manually or from a scheduler. The scheduler is outside
Docker Compose, so the load test does not change the Flask or Nginx services.

## Architecture

```text
k6 or browser -> Nginx :8080 (published host port) -> Flask/Gunicorn :8000
                                                           (private network)
```

Nginx is the only service published to the host. It serves the static page
from `nginx/html/index.html` and reverse-proxies `/api/` and `/health` to the
Flask container. The Flask container is available only inside the Docker
network.

## Start the application

```bash
docker compose up -d --build
docker compose ps
./scripts/verify.sh
```

The application is available at:

```text
http://localhost:8080
```

## Endpoints

| Path | Method | Expected response |
|---|---|---|
| `/nginx-health` | GET | 200, served by Nginx |
| `/health` | GET | 200 |
| `/api/ok` | GET | 200 |
| `/api/items` | POST | 201 |
| `/api/no-content` | GET | 204 |
| `/api/bad-request` | GET | 400 |
| `/api/unauthorized` | GET | 401 |
| `/api/forbidden` | GET | 403 |
| `/api/not-found` | GET | 404 |
| `/api/rate-limited` | GET | 429 |
| `/api/error` | GET | 500 |
| `/api/bad-gateway` | GET | 502 |
| `/api/unavailable` | GET | 503 |
| `/api/slow?seconds=2` | GET | 200 after a delay |
| `/api/random` | GET | Weighted mix of 2xx, 4xx, and 5xx |

For example:

```bash
curl -i http://localhost:8080/api/error
```

The response must still be HTTP 500:

```text
HTTP/1.1 500 INTERNAL SERVER ERROR
```

## Run the k6 load generator

Install k6, start the application, and run:

```bash
k6 run k6/load-test.js
```

The current k6 configuration is:

```text
virtual users: 5
duration:      1 minute
target:        http://host.docker.internal:8080/
pause:         1 second
```

## Run k6 on a schedule

I schedule the same k6 command outside Docker Compose. For example, on Linux
or macOS, I can run it every 15 minutes with cron:

```cron
*/15 * * * * cd /path/to/t1-1-nginx-flask && k6 run k6/load-test.js >> k6/load-test.log 2>&1
```

On Windows, I create a Task Scheduler task that runs:

```text
k6 run C:\path\to\t1-1-nginx-flask\k6\load-test.js
```

I set the trigger interval in Task Scheduler, for example every 15 minutes,
and keep Docker Compose running before the task starts.

## Logs and additional traffic

Nginx writes structured JSON access logs containing the request status,
upstream status, and request time:

```bash
docker compose logs nginx
```

I can also generate a short mixed traffic burst without k6:

```bash
./scripts/traffic.sh 100
```

## Tests

Run the Flask tests without Docker:

```bash
make test
```

Run the endpoint verification script through Nginx:

```bash
./scripts/verify.sh
```

## Troubleshooting

1. **Port 8080 is already in use** - set `HOST_PORT=9090` in `.env`, then
   restart the services.
2. **Every request returns 502** - check the Flask container with
   `docker compose logs app`.
3. **The Nginx configuration change is not applied** - recreate Nginx with
   `docker compose up -d --force-recreate nginx`.
4. **The scheduled k6 run fails** - confirm Docker Compose is running and
   verify that the target URL is reachable from the machine running k6.

## Stop and clean up

```bash
docker compose down
```

I keep the k6 script in the project so the load test is repeatable and can be
run manually or from my scheduled task whenever I need fresh traffic.

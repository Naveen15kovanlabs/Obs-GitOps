# Migrate Promtail → Grafana Alloy

## What this task is about

This is task T1.3 from Week 1 (Logs). I had to replace Promtail with Grafana Alloy and make sure the logs kept flowing to Loki.

Promtail is the old log collector for Loki, and Grafana is moving everything over to Alloy. I wanted to switch without losing any logs on the way.

## What I built

I set up a small logging stack on one EC2 instance with Docker Compose:

- **Loki** stores the logs
- **Grafana** shows them
- **Alloy** collects the system logs and the Docker container logs and sends them to Loki

## How I did it

1. **Set up the stack with Promtail first.** I started Loki, Grafana and Promtail with Docker Compose on my EC2 instance. Promtail collected the system logs from `/var/log` and the Docker container logs.
2. **Checked the logs in Grafana.** I made sure Loki showed up as a data source (I added it through a provisioning file, so Grafana sets it up by itself). Then I ran queries in Explore to see the logs.
3. **Added Alloy next to Promtail.** I wrote an Alloy config that reads the same files and uses the same labels (`job` and `host`). For a while both ran together.
4. **Compared them.** I gave each one a temporary `collector` label, `promtail` or `alloy`, so I could compare their log counts in Grafana for the same time window.
5. **Switched over.** The counts matched, so I stopped Promtail and removed it. New logs kept arriving from Alloy.
6. **Cleaned up.** I deleted the Promtail files and the temporary label, put Alloy into the main `docker-compose.yml`, and pushed everything to GitHub.

## How I checked that it worked

I used these queries in Grafana Explore with the Loki data source.

Promtail only:
```
{collector="promtail"}
```

Both together, to compare the counts:
```
sum by (collector, job) (count_over_time({collector=~"alloy|promtail"}[10m]))
```

Alloy only:
```
{collector="alloy"}
```

While both ran, the counts for the same job were close. After I removed Promtail, new logs kept coming in from Alloy only.

My screenshots of these checks are in the `images` folder.

## Folder layout

```
docker-compose.yml                         Loki, Grafana and Alloy
loki/loki-config.yaml                      Loki settings (7 day retention)
alloy/config.alloy                         Alloy settings (what to collect, where to send)
grafana/provisioning/datasources/loki.yml  adds Loki to Grafana automatically
.env.example                               template for the secrets file
images/                                    my screenshots from the checks
learnings.md                               what I learned
```

## How to run it

You need an Ubuntu EC2 instance with Docker and the Compose plugin, and your user in the `docker` group.

1. Clone the repo and go into this folder.
2. Copy `.env.example` to `.env` and set your own password. The real `.env` is in `.gitignore`, so it never gets pushed:
```
cp .env.example .env
```
3. Check the compose file and start everything:
```
docker compose config > /dev/null && echo FILES-OK
docker compose up -d
docker compose ps
```
You should see `loki`, `grafana` and `alloy` as Up.

4. Open `http://<EC2_PUBLIC_IP>:3000`, log in, go to **Explore**, choose **Loki**, and run `{job="varlogs"}` or `{job="docker"}`.

In the security group I only opened TCP 3000, and only to my own IP. Loki (3100) and Alloy (12345) stay closed.

## Problems I ran into

- **`docker: not found`:** Docker wasn't installed on the instance yet, so I installed it first.
- **`permission denied` on Docker:** I connected through Session Manager, so my user was `ssm-user` and not `ubuntu`. I added `ssm-user` to the `docker` group and opened a new session.
- **Pasted commands got merged:** my terminal joined the lines together, so I pasted one block at a time.
- **`no such service: alloy`:** Compose only knows the services in the files I give it with `-f`, so I had to name the right file.
- **Git push rejected:** GitHub had newer commits than my local copy, so I ran `git pull --rebase` before pushing.

## Notes

- I never commit `.env`. I check `git status` before every commit.
- Alloy runs as root so it can read `/var/log` and the Docker log files.
- I set `tail_from_end = true` in the Alloy config so it doesn't send old lines again that Promtail already sent.
- Loki keeps logs for 7 days. That's the `retention_period` in `loki/loki-config.yaml`.

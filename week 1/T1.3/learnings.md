# Learnings: Promtail → Grafana Alloy (T1.3)

**What I did**

I set up Loki, Grafana and Promtail on an EC2 instance using Docker Compose. Then I added Alloy next to Promtail, checked both were sending the same logs, stopped Promtail and kept only Alloy. The Alloy config went to GitHub.

**What I learned**

1. **Docker wasn't installed, and then it didn't work for my user.** `docker: not found` just meant I had to install it first. After that I got `permission denied` on the Docker socket, because my user wasn't in the `docker` group yet.

2. **I was logged in as `ssm-user`, not `ubuntu`.** I connected through Session Manager, so `$USER` was empty and my `usermod` command did nothing at first. I had to run `whoami` to find the real username. Group changes also only apply to a new session, so I had to reconnect.

3. **Pasting many commands at once can break things.** My terminal merged lines together, so some commands never ran properly. Pasting one block at a time and checking with `ls` and `cat` fixed it.

4. **Compose files can be stacked.** I used a base file (Loki and Grafana) plus extra files for Promtail and Alloy, with `-f file1 -f file2`. If you leave out a file, Compose doesn't know that service. That's why `docker compose stop alloy` said "no such service" and why I saw the "orphan containers" warning. The warning looked scary but was harmless.

5. **Containers talk to each other by name.** Grafana reaches Loki at `http://loki:3100`, not `localhost`. I didn't open Loki's port to the outside, and only Grafana's port 3000 was open to my IP.

6. **Grafana can add the Loki data source by itself.** A small provisioning file did it, so I only had to check it in the UI.

7. **A `collector` label made the comparison easy.** Promtail tagged its logs `collector=promtail` and Alloy tagged its logs `collector=alloy`. Then I could compare counts per collector in Grafana, instead of guessing.

8. **Old logs stay in Loki.** Switching tools didn't delete anything, but older lines had no `collector` label. That's why the graph had a big spike that I had to filter out of the queries.

9. **`tail_from_end = true` avoids duplicates.** Without it, Alloy could re-read old lines that Promtail had already sent.

10. **Never put secrets in Git.** The `.env` file with the Grafana password stays on the server and in `.gitignore`. I checked `git status` before every commit.

**How I knew it worked**

Same log counts from both collectors while they ran together. After I stopped Promtail, new logs kept arriving from Alloy only.

**Next time**

I'd check my username and the docker group first, paste commands one at a time, and add a label like `collector` from the start when migrating between tools.
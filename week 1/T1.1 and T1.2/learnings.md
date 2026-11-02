# My Learnings

I deployed a small Flask app behind Nginx by using Docker Compose. The Flask
app runs inside a private Docker network, and Nginx is the public entry point
on port 8080.

I learned how Nginx can be used as a reverse proxy and as a static file
server. Nginx serves the browser test page directly, forwards `/api/` and
`/health` requests to Flask, keeps the Flask service private, and provides a
separate `/nginx-health` endpoint. I also learned that Nginx can add useful
request headers, expose health checks, and write structured JSON access logs.

I explored k6 and the `k6/load-test.js` file. The script creates five virtual
users, runs the test for one minute, sends requests to the application through
Nginx, and waits one second between requests. I learned that the JavaScript
file defines the k6 test options and that the default function is repeated by
each virtual user during the test.

I analyzed the Docker logs to understand the traffic moving through the
containers. I checked the Nginx access logs and the Flask container logs to
compare the incoming request, HTTP status, upstream status, and request time.
This helped me understand how Nginx forwards requests and how Flask responses
appear in the logs.

I also analyzed the metrics from the one-minute k6 load test. I looked at the
number of requests, request duration, response timing, throughput, and failed
requests. This helped me understand how a small load test can show the
behavior and performance of the application while traffic is passing through
Nginx.
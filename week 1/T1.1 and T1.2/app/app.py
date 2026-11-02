"""Sample Flask app that deliberately returns mixed 2xx / 4xx / 5xx responses.

Used for the observability / DevOps training roadmap (Task T1.1).
"""
import os
import random
import time

from flask import Flask, jsonify, request

app = Flask(__name__)
START_TIME = time.time()
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

# Weighted outcomes for /api/random  (status, weight)
RANDOM_OUTCOMES = [(200, 60), (201, 5), (400, 8), (401, 4), (404, 8), (429, 3), (500, 8), (503, 4)]


def reply(status, message, **extra):
    body = {"status": status, "message": message, **extra}
    return jsonify(body), status


@app.get("/")
def index():
    return reply(200, "Sample app is up", version=APP_VERSION, endpoints=sorted(
        str(r) for r in app.url_map.iter_rules() if r.endpoint != "static"))


# ---- 2xx ----------------------------------------------------------------
@app.get("/health")
def health():
    return reply(200, "healthy", uptime_seconds=round(time.time() - START_TIME, 1))


@app.get("/api/ok")
def ok():
    return reply(200, "OK")


@app.post("/api/items")
def create_item():
    return reply(201, "Created", item=request.get_json(silent=True) or {})


@app.get("/api/no-content")
def no_content():
    return "", 204


# ---- 4xx ----------------------------------------------------------------
@app.get("/api/bad-request")
def bad_request():
    return reply(400, "Bad request - invalid input")


@app.get("/api/unauthorized")
def unauthorized():
    return reply(401, "Unauthorized - missing credentials")


@app.get("/api/forbidden")
def forbidden():
    return reply(403, "Forbidden - not allowed")


@app.get("/api/not-found")
def not_found_endpoint():
    return reply(404, "Resource not found")


@app.get("/api/rate-limited")
def rate_limited():
    return reply(429, "Too many requests")


# ---- 5xx ----------------------------------------------------------------
@app.get("/api/error")
def server_error():
    return reply(500, "Internal server error (simulated)")


@app.get("/api/bad-gateway")
def bad_gateway():
    return reply(502, "Bad gateway (simulated)")


@app.get("/api/unavailable")
def unavailable():
    return reply(503, "Service unavailable (simulated)")


@app.get("/api/slow")
def slow():
    delay = min(float(request.args.get("seconds", 2)), 10)
    time.sleep(delay)
    return reply(200, "Slow response", delay_seconds=delay)


# ---- mixed --------------------------------------------------------------
@app.get("/api/random")
def random_status():
    codes, weights = zip(*RANDOM_OUTCOMES)
    status = random.choices(codes, weights=weights, k=1)[0]
    return reply(status, "Random outcome")


@app.errorhandler(404)
def handle_404(_e):
    return reply(404, "Route not found", path=request.path)


@app.errorhandler(405)
def handle_405(_e):
    return reply(405, "Method not allowed", path=request.path)


@app.errorhandler(Exception)
def handle_unexpected(_e):
    return reply(500, "Unexpected server error")

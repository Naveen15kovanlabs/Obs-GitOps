import asyncio
import time

from fastapi import FastAPI
from prometheus_client import Counter, Gauge, Histogram, make_asgi_app

app = FastAPI(title="FastAPI Application Instrumentation")

# Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"]
)

REQUESTS_IN_FLIGHT = Gauge(
    "http_requests_in_flight",
    "Number of HTTP requests currently being processed"
)

# Sample application data
users = [
    {"id": 1, "name": "Naveen"}
]


@app.middleware("http")
async def metrics_middleware(request, call_next):

    # Do not instrument Prometheus scrape requests
    if request.url.path.rstrip("/") == "/metrics":
        return await call_next(request)

    start_time = time.perf_counter()
    REQUESTS_IN_FLIGHT.inc()
    status_code = "500"

    try:
        response = await call_next(request)
        status_code = str(response.status_code)
        return response

    finally:
        duration = time.perf_counter() - start_time

        route = request.scope.get("route")
        endpoint = route.path if route else request.url.path

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status=status_code
        ).inc()

        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=endpoint
        ).observe(duration)

        REQUESTS_IN_FLIGHT.dec()


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/users")
async def get_users():
    return users


@app.post("/users")
async def create_user():
    user = {
        "id": len(users) + 1,
        "name": f"User {len(users) + 1}"
    }
    users.append(user)
    return user


@app.get("/slow")
async def slow_endpoint():
    await asyncio.sleep(10)
    return {"message": "Slow request completed"}


# Prometheus metrics endpoint: /metrics/
app.mount("/metrics", make_asgi_app())

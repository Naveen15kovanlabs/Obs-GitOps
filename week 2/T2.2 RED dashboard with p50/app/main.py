from fastapi import FastAPI, HTTPException, Request
from prometheus_client import Counter, Histogram, make_asgi_app
import time

app = FastAPI(title="FastAPI RED Monitoring")

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"]
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request processing duration in seconds",
    ["method", "endpoint", "status_code"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10)
)

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    if request.url.path.startswith("/metrics"):
        return await call_next(request)

    method = request.method
    endpoint = request.url.path
    start_time = time.time()

    response = await call_next(request)
    duration = time.time() - start_time
    status_code = str(response.status_code)

    REQUEST_COUNT.labels(
        method=method,
        endpoint=endpoint,
        status_code=status_code
    ).inc()

    REQUEST_DURATION.labels(
        method=method,
        endpoint=endpoint,
        status_code=status_code
    ).observe(duration)

    return response

@app.get("/")
async def home():
    return {"message": "FastAPI RED Monitoring Application"}

@app.get("/items")
async def get_items():
    return {"items": ["item-1", "item-2", "item-3"]}

@app.get("/work")
async def work(delay_ms: int = 100):
    time.sleep(max(0, min(delay_ms, 5000)) / 1000)
    return {"message": "Work completed", "delay_ms": delay_ms}

@app.get("/error")
async def generate_error():
    raise HTTPException(status_code=500, detail="Test server error")

@app.get("/health")
async def health():
    return {"status": "healthy"}

app.mount("/metrics", make_asgi_app())

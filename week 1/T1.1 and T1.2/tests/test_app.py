import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
import pytest
from app import app

@pytest.fixture
def client():
    return app.test_client()

@pytest.mark.parametrize("method,path,status", [
    ("get", "/health", 200), ("get", "/api/ok", 200), ("post", "/api/items", 201),
    ("get", "/api/no-content", 204), ("get", "/api/bad-request", 400),
    ("get", "/api/unauthorized", 401), ("get", "/api/forbidden", 403),
    ("get", "/api/not-found", 404), ("get", "/api/rate-limited", 429),
    ("get", "/api/error", 500), ("get", "/api/bad-gateway", 502),
    ("get", "/api/unavailable", 503), ("get", "/nope", 404),
])
def test_status(client, method, path, status):
    assert getattr(client, method)(path).status_code == status

def test_random_is_mixed(client):
    classes = {client.get("/api/random").status_code // 100 for _ in range(300)}
    assert {2, 4, 5} <= classes

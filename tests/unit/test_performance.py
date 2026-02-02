from fastapi.testclient import TestClient
import time
from src.banking_api.main import app

client = TestClient(app)


def test_api_speed():
    start_time = time.time()
    response = client.get("/api/transactions/")
    end_time = time.time()
    duration = end_time - start_time

    assert response.status_code == 200
    assert duration < 1.0


def test_stats_speed():
    start_time = time.time()
    client.get("/api/stats/overview")
    end_time = time.time()
    duration = end_time - start_time
    assert duration < 1.0

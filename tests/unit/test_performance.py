import os
import time
import pytest
from fastapi.testclient import TestClient
from src.banking_api.main import app

client = TestClient(app)

PERF_THRESHOLD_SECONDS = float(os.getenv("PERF_THRESHOLD_SECONDS", "1.0"))
RUN_PERF_TESTS = os.getenv("RUN_PERF_TESTS") == "1"


@pytest.mark.performance
def test_api_speed():
    if not RUN_PERF_TESTS:
        pytest.skip("Performance tests disabled; set RUN_PERF_TESTS=1 to run")

    start_time = time.time()
    response = client.get("/api/transactions/")
    end_time = time.time()
    duration = end_time - start_time

    assert response.status_code == 200
    assert duration < PERF_THRESHOLD_SECONDS


@pytest.mark.performance
def test_stats_speed():
    if not RUN_PERF_TESTS:
        pytest.skip("Performance tests disabled; set RUN_PERF_TESTS=1 to run")

    start_time = time.time()
    response = client.get("/api/stats/overview")
    end_time = time.time()
    duration = end_time - start_time

    assert response.status_code == 200
    assert duration < PERF_THRESHOLD_SECONDS

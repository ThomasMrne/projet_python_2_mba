from fastapi.testclient import TestClient
from src.banking_api.main import app

client = TestClient(app)


def test_invalid_page_param():
    response = client.get("/api/transactions/search?page=abc")
    assert response.status_code == 422


def test_negative_limit():
    response = client.get("/api/transactions/search?limit=-5")
    assert response.status_code == 422

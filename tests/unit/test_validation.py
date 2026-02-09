from fastapi.testclient import TestClient
from src.banking_api.main import app

# Initialisation du client de test FastAPI
client = TestClient(app)


def test_invalid_page_param():
    """Vérifie que l'API rejette un numéro de page non numérique."""
    response = client.get("/api/transactions/search?page=abc")
    assert response.status_code == 422


def test_negative_limit():
    """Vérifie que l'API rejette une limite de résultats négative."""
    response = client.get("/api/transactions/search?limit=-5")
    # L'API doit renvoyer une erreur de validation
    assert response.status_code == 422

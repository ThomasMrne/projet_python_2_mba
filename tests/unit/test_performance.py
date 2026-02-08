import time
import pytest
from fastapi.testclient import TestClient
from src.banking_api.main import app
from src.banking_api.services.data_loader import load_dataset

# On s'assure que les données sont prêtes
load_dataset()
client = TestClient(app)

# Seuil de performance (ajusté car 13M de lignes c'est lourd !)
PERF_THRESHOLD_SECONDS = 2.0


@pytest.mark.performance
def test_api_speed():
    """Mesure la vitesse de récupération des transactions."""
    start_time = time.time()
    # On ajoute une limite pour ne pas charger 13M de lignes dans le JSON
    response = client.get("/api/transactions?limit=10")
    duration = time.time() - start_time

    assert response.status_code == 200
    assert duration < PERF_THRESHOLD_SECONDS


@pytest.mark.performance
def test_stats_speed():
    """Mesure la vitesse du service de statistiques."""
    start_time = time.time()
    # Vérifie que l'URL /api/stats/overview correspond bien à ton router
    response = client.get("/api/stats/overview")
    duration = time.time() - start_time

    assert response.status_code == 200
    assert duration < PERF_THRESHOLD_SECONDS

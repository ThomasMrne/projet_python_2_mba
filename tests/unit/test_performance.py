import time
from fastapi.testclient import TestClient
from src.banking_api.main import app
from src.banking_api.services.data_loader import load_dataset

load_dataset()
client = TestClient(app)

def test_performance_100_transactions():
    """
    Vérifie que récupérer 100 transactions prend moins de 500ms.
    Critère PDF : 'latence max < 500ms pour 100 transactions filtrées'
    """
    start_time = time.time()
    
    # On demande 100 transactions
    response = client.get("/api/transactions?limit=100")
    
    end_time = time.time()
    duration = end_time - start_time
    
    assert response.status_code == 200
    # La durée doit être inférieure à 0.5 seconde
    assert duration < 0.5, f"Trop lent ! Temps: {duration}s"
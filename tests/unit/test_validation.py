from fastapi.testclient import TestClient
from src.banking_api.main import app

client = TestClient(app)

def test_validation_error_json():
    """
    Vérifie que l'API rejette un JSON mal formé.
    Critère PDF : 'vérification du format des entrées JSON'
    """
    # On envoie "cinq cents" (texte) au lieu de 500 (chiffre) pour le montant
    mauvais_json = {
        "min_amount": "cinq cents" 
    }
    
    response = client.post("/api/transactions/search", json=mauvais_json)
    
    # On attend une erreur 422 (Unprocessable Entity)
    assert response.status_code == 422
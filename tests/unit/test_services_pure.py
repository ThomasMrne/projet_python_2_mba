from src.banking_api.services import stats_service, fraud_detection_service
from src.banking_api.services.data_loader import load_dataset

# On charge les données pour que les services fonctionnent
load_dataset()

def test_stats_service_pure():
    """Test direct de la fonction de calcul (sans passer par l'API)"""
    stats = stats_service.get_global_stats()
    assert stats["total_transactions"] > 0
    assert isinstance(stats["avg_amount"], float)

def test_fraud_service_pure():
    """Test direct de la fonction de prédiction"""
    # On teste la logique métier pure
    result = fraud_detection_service.predict_fraud(amount=50000, type="Online Transaction")
    assert result["isFraud"] is True
    assert result["risk_level"] == "High"
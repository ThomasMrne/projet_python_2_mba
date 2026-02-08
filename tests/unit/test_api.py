import pytest
from fastapi.testclient import TestClient
from src.banking_api.main import app
from src.banking_api.services.data_loader import load_dataset, get_data

# Initialisation du dataset pour les tests
load_dataset()
client = TestClient(app)


def test_route_1_list_transactions():
    """Route 1: Liste"""
    response = client.get("/api/transactions?limit=5")
    assert response.status_code == 200
    data = response.json()
    if data["total_items"] > 0:
        assert len(data["transactions"]) > 0
    else:
        pytest.skip("Dataset vide")


def test_route_2_transaction_detail():
    """Route 2: Détail par ID"""
    res_list = client.get("/api/transactions?limit=1").json()
    tx_list = res_list.get("transactions", [])
    if not tx_list:
        pytest.skip("Pas de données")

    tx_id = tx_list[0]["id"]
    response = client.get(f"/api/transactions/{tx_id}")
    assert response.status_code == 200
    assert str(response.json()["id"]) == str(tx_id)


def test_route_3_transaction_search():
    """Route 3: Recherche"""
    response = client.post("/api/transactions/search", json={"min_amount": 0})
    assert response.status_code == 200
    if response.json()["total_items"] > 0:
        assert len(response.json()["transactions"]) > 0


def test_route_5_recent_transactions():
    """Route 5: Récentes"""
    response = client.get("/api/transactions/recent?n=5")
    assert response.status_code == 200
    if get_data().shape[0] >= 5:
        assert len(response.json()) == 5


def test_route_6_delete_transaction():
    """Route 6: Suppression"""
    data = client.get("/api/transactions?limit=1").json()
    if data.get("transactions"):
        tx_id = data["transactions"][0]["id"]
        assert client.delete(f"/api/transactions/{tx_id}").status_code == 200
    else:
        pytest.skip("Rien à supprimer")


def test_route_7_transactions_by_customer():
    """Route 7: Par Client"""
    response = client.get("/api/transactions?limit=1")
    txs = response.json().get("transactions", [])

    if not txs or "client_id" not in txs[0]:
        pytest.skip("ID client manquant")

    cid = txs[0]["client_id"]
    response = client.get(f"/api/transactions/by-customer/{cid}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_route_16_customers_list():
    """Route 16: Liste Clients (Format Dict)"""
    response = client.get("/api/customers?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["customers"], dict)
    if data["total_items"] > 0:
        assert len(data["customers"]) > 0


def test_route_17_customer_profile():
    """Route 17: Profil Client"""
    top_data = client.get("/api/customers/top?n=1").json()
    if not top_data:
        pytest.skip("Pas de clients")

    cid = list(top_data.keys())[0]
    response = client.get(f"/api/customers/{cid}")
    assert response.status_code == 200
    assert str(response.json()["id"]) == str(cid)


def test_route_18_top_customers():
    """Route 18: Top Clients (Format Dict)"""
    response = client.get("/api/customers/top?n=3")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)

    df = get_data()
    if not df.empty and "client_id" in df.columns:
        if len(df["client_id"].unique()) >= 3:
            assert len(data) == 3
    else:
        assert isinstance(data, dict)


def test_route_19_health():
    """Route 19: Health"""
    assert client.get("/api/system/health").json()["status"] == "ok"

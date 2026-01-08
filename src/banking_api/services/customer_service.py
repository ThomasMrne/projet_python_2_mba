import math
from src.banking_api.services.data_loader import get_data


def get_all_customers(page=1, limit=10):
    """
    Route 16: Liste des clients uniques (paginée).
    """
    df = get_data()
    if df.empty:
        return {"page": page, "total_items": 0, "total_pages": 0, "customers": []}

    # On récupère la liste des IDs clients uniques
    unique_clients = df["client_id"].unique()
    total_items = len(unique_clients)

    # Pagination manuelle
    total_pages = math.ceil(total_items / limit)
    start = (page - 1) * limit
    end = start + limit

    page_clients = unique_clients[start:end]

    # Formatage
    results = [{"id": str(cid), "name": f"Client_{cid}"} for cid in page_clients]

    return {
        "page": page,
        "total_pages": total_pages,
        "total_items": total_items,
        "customers": results,
    }


def get_customer_profile(customer_id: str):
    """
    Route 17: Profil détaillé d'un client.
    """
    df = get_data()
    try:
        cid = int(customer_id)
        # On filtre toutes les transactions de ce client
        client_tx = df[df["client_id"] == cid]

        if client_tx.empty:
            return None

        total_tx = len(client_tx)
        avg_amt = client_tx["amount"].abs().mean()

        # Est-ce qu'il a des transactions avec erreurs (fraude potentielle) ?
        has_fraud = False
        if "errors" in df.columns:
            fraud_rows = client_tx[
                (client_tx["errors"] != 0)
                & (client_tx["errors"] != "0")
                & (client_tx["errors"].notna())
            ]
            has_fraud = not fraud_rows.empty

        return {
            "id": str(cid),
            "transactions_count": int(total_tx),
            "avg_amount": float(round(avg_amt, 2)),
            "fraudulent": has_fraud,
            # On essaie de récupérer les dates min/max si la colonne existe
            "first_seen": (
                str(client_tx["date"].min()) if "date" in df.columns else "N/A"
            ),
            "last_seen": (
                str(client_tx["date"].max()) if "date" in df.columns else "N/A"
            ),
        }
    except ValueError:
        return None


def get_top_customers(n=10):
    """
    Route 18: Top clients par volume d'argent dépensé.
    """
    df = get_data()
    if df.empty:
        return []

    # On copie pour éviter les warnings pandas
    wdf = df[["client_id", "amount"]].copy()
    wdf["amount"] = wdf["amount"].abs()

    # Group By Client -> Somme des montants -> Tri Décroissant -> Prendre les N premiers
    top = wdf.groupby("client_id")["amount"].sum().sort_values(ascending=False).head(n)

    results = []
    for client_id, total_amount in top.items():
        results.append(
            {"id": str(client_id), "total_spent": float(round(total_amount, 2))}
        )

    return results

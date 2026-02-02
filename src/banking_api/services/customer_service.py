from typing import Dict, Any

from src.banking_api.services.data_loader import get_data


def get_all_customers(page: int = 1, limit: int = 10) -> Dict[str, Any]:
    """Route 16: Liste des clients uniques (paginée)."""
    # Sécurité : On force des valeurs positives
    page = max(1, page)
    limit = max(1, min(limit, 100))

    df = get_data()

    if df.empty or "client_id" not in df.columns:
        return {
            "page": page,
            "total_items": 0,
            "customers": []
        }

    # On récupère la liste unique des clients
    unique_clients = df["client_id"].dropna().unique()
    total_items = len(unique_clients)

    # Pagination manuelle sur la liste
    start = (page - 1) * limit
    end = start + limit
    page_clients = unique_clients[start:end]

    customers_list = []
    for cid in page_clients:
        # On essaie de trouver le nom s'il existe
        client_rows = df[df["client_id"] == cid]
        if not client_rows.empty and "nameOrig" in df.columns:
            cname = client_rows.iloc[0]["nameOrig"]
        else:
            cname = f"Client_{cid}"

        customers_list.append({
            "id": int(cid),
            "name": str(cname)
        })

    return {
        "page": page,
        "total_items": total_items,
        "customers": customers_list
    }


def get_customer_profile(customer_id: int):
    """Route 17: Profil complet d'un client."""
    df = get_data()

    if df.empty or "client_id" not in df.columns:
        return None

    # Conversion en string pour comparaison
    customer_df = df[df["client_id"].astype(str) == str(customer_id)]

    if customer_df.empty:
        return None

    # Infos de base (on prend la première ligne trouvée)
    first_row = customer_df.iloc[0]
    name = first_row.get("nameOrig", f"Client_{customer_id}")

    # Stats calculées
    total_spent = customer_df[customer_df["amount"] < 0]["amount"].sum()
    total_received = customer_df[customer_df["amount"] > 0]["amount"].sum()
    balance = customer_df["amount"].sum()

    return {
        "id": customer_id,
        "name": name,
        "stats": {
            "transaction_count": len(customer_df),
            "total_spent": abs(round(total_spent, 2)),
            "total_received": round(total_received, 2),
            "current_balance": round(balance, 2)
        }
    }


def get_top_customers(n: int = 5):
    """Route 18: Top N clients par volume de transactions."""
    df = get_data()

    if df.empty or "client_id" not in df.columns:
        return []

    # On compte les occurrences de chaque client_id
    top_series = df["client_id"].value_counts().head(n)

    results = []
    for cid, count in top_series.items():
        results.append({
            "id": int(cid),
            "transaction_count": int(count)
        })

    return results

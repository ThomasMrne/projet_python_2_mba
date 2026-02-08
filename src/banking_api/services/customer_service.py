from typing import Dict, Any
from src.banking_api.services.data_loader import get_data


def get_all_customers(page: int = 1, limit: int = 10) -> Dict[str, Any]:
    """Route 16: Liste des clients uniques (paginée)."""
    page = max(1, page)
    limit = max(1, min(limit, 100))
    df = get_data()

    if df.empty or "client_id" not in df.columns:
        return {
            "page": page,
            "total_items": 0,
            "customers": {}
        }

    unique_clients = df["client_id"].dropna().unique()
    total_items = len(unique_clients)

    start = (page - 1) * limit
    end = start + limit
    page_clients = unique_clients[start:end]

    customers_dict = {}
    for cid in page_clients:
        client_rows = df[df["client_id"] == cid]
        if not client_rows.empty and "nameOrig" in df.columns:
            cname = client_rows.iloc[0]["nameOrig"]
        else:
            cname = f"Client_{cid}"

        # Conversion explicite pour Mypy
        customers_dict[int(str(cid))] = {
            "id": int(str(cid)),
            "name": str(cname)
        }

    return {
        "page": page,
        "total_items": total_items,
        "total_pages": (total_items + limit - 1) // limit,
        "customers": customers_dict
    }


def get_customer_profile(customer_id: int) -> Any:
    """Route 17: Profil complet d'un client."""
    df = get_data()

    if df.empty or "client_id" not in df.columns:
        return None

    # Conversion en string
    customer_df = df[df["client_id"].astype(str) == str(customer_id)]

    if customer_df.empty:
        return None

    first_row = customer_df.iloc[0]
    name = first_row.get("nameOrig", f"Client_{customer_id}")

    total_spent = customer_df[customer_df["amount"] < 0]["amount"].sum()
    total_recv = customer_df[customer_df["amount"] > 0]["amount"].sum()
    balance = customer_df["amount"].sum()

    return {
        "id": customer_id,
        "name": name,
        "stats": {
            "transaction_count": len(customer_df),
            "total_spent": abs(round(float(total_spent), 2)),
            "total_received": round(float(total_recv), 2),
            "current_balance": round(float(balance), 2)
        }
    }


def get_top_customers(n: int = 5) -> Dict[int, int]:
    """Route 18: Top N clients par volume de transactions."""
    n = max(1, n)
    df = get_data()

    if df.empty or "client_id" not in df.columns:
        return {}

    top_series = df["client_id"].value_counts().head(n)

    # Retourne un dictionnaire {id_client: nombre_transactions}
    return {int(str(cid)): int(count) for cid, count in top_series.items()}

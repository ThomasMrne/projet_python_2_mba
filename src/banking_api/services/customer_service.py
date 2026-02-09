from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
from src.banking_api.services.data_loader import get_data


def get_all_customers(page: int = 1, limit: int = 10) -> Dict[str, Any]:
    """Route 16: Récupère la liste paginée des clients sans erreur de type."""
    df: pd.DataFrame = get_data()

    unique_clients: np.ndarray = np.array([])
    if not df.empty and "client_id" in df.columns:
        unique_clients = df["client_id"].dropna().unique()

    total_items: int = len(unique_clients)

    start: int = (page - 1) * limit
    page_clients: np.ndarray = unique_clients[start:start + limit]

    customers_dict: Dict[int, Any] = {}
    for cid in page_clients:
        # Conversion robuste ID
        safe_id: int = int(float(str(cid)))

        rows = df[df["client_id"] == cid]
        name = f"Client_{cid}"
        if not rows.empty:
            name = rows.iloc[0].get("nameOrig", f"Client_{cid}")

        customers_dict[safe_id] = {
            "id": safe_id,
            "name": str(name)
        }

    return {
        "page": page,
        "total_items": total_items,
        "total_pages": (total_items + limit - 1) // limit if limit > 0 else 0,
        "customers": customers_dict
    }


def get_customer_profile(customer_id: int) -> Optional[Dict[str, Any]]:
    """Route 17: Analyse l'historique financier d'un client."""
    df: pd.DataFrame = get_data()

    if df.empty or "client_id" not in df.columns:
        return None

    # Filtrage
    c_df: pd.DataFrame = df[df["client_id"].astype(str) == str(customer_id)]

    if c_df.empty:
        return None

    first_row = c_df.iloc[0]
    name = first_row.get("nameOrig", f"Client_{customer_id}")

    # Calculs agrégés
    spent = float(c_df[c_df["amount"] < 0]["amount"].sum())
    recv = float(c_df[c_df["amount"] > 0]["amount"].sum())
    balance = float(c_df["amount"].sum())

    return {
        "id": customer_id,
        "name": str(name),
        "stats": {
            "transaction_count": len(c_df),
            "total_spent": abs(round(spent, 2)),
            "total_received": round(recv, 2),
            "current_balance": round(balance, 2)
        }
    }


def get_top_customers(n: int = 5) -> Dict[int, int]:
    """Route 18: Top N clients avec conversion robuste (CoderRabbit)."""
    df: pd.DataFrame = get_data()
    if df.empty or "client_id" not in df.columns:
        return {}

    top_series = df["client_id"].value_counts().head(n)

    return {
        int(float(str(cid))): int(count)
        for cid, count in top_series.items()
    }

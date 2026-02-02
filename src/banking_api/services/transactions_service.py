import math
import pandas as pd
from typing import List, Optional, Dict, Any

from src.banking_api.services.data_loader import get_data


def get_all_transactions(limit: int = 100) -> List[dict]:
    """Récupère une liste simple de transactions (limitée)."""
    df = get_data()
    if df.empty:
        return []

    subset = df.head(limit)
    return [map_row_to_transaction(row) for _, row in subset.iterrows()]


def get_transaction_by_id(search_id: int):
    """Récupère une transaction unique par son ID."""
    df = get_data()
    if df.empty:
        return None

    if "id" not in df.columns:
        return None

    row = df[df["id"].astype(str) == str(search_id)]

    if row.empty:
        return None

    return map_row_to_transaction(row.iloc[0])


def map_row_to_transaction(row) -> Dict[str, Any]:
    """Transforme une ligne DataFrame en dictionnaire Transaction."""
    item = row.to_dict()

    for key, value in item.items():
        if pd.isna(value):
            item[key] = None

    m_state = item.get("merchant_state")
    if m_state in (0, "0") or pd.isna(m_state):
        item["merchant_state"] = None

    err = item.get("errors")
    if err in (0, "0") or pd.isna(err):
        item["errors"] = None

    if item.get("zip") is not None:
        try:
            item["zip"] = float(item["zip"])
        except ValueError:
            item["zip"] = None

    chip_val = item.get("use_chip")
    if "type" not in item:
        if chip_val is not None:
            item["type"] = str(chip_val)
        else:
            item["type"] = "Unknown Transaction"

    if "nameOrig" not in item:
        client_id = item.get('client_id')
        if client_id is not None:
            item["nameOrig"] = f"Client_{client_id}"
        else:
            item["nameOrig"] = "Client_Unknown"

    if "nameDest" not in item:
        merch_id = item.get('merchant_id')
        if merch_id is not None:
            item["nameDest"] = f"Merchant_{merch_id}"
        else:
            item["nameDest"] = "Merchant_Unknown"

    raw_amount = item.get('amount')
    if raw_amount is None:
        raw_amount = 0.0
    item["formatted_amount"] = f"{raw_amount:.2f} €"

    item["id"] = str(item.get("id", "0"))
    item["date"] = str(item.get("date", ""))

    return item


def get_transactions(
    page: int,
    limit: int,
    type: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
):
    """Récupère les transactions avec pagination et filtres."""
    df = get_data()

    if df.empty:
        return {
            "page": page,
            "total_pages": 0,
            "total_items": 0,
            "transactions": []
        }

    page = max(1, page)
    limit = max(1, limit)

    filtered = df

    if type and "use_chip" in filtered.columns:
        filtered = filtered[filtered["use_chip"] == type]

    if min_amount is not None and "amount" in filtered.columns:
        filtered = filtered[filtered["amount"].abs() >= min_amount]

    if max_amount is not None and "amount" in filtered.columns:
        filtered = filtered[filtered["amount"].abs() <= max_amount]

    total_items = len(filtered)

    total_pages = math.ceil(total_items / limit)

    start_idx = (page - 1) * limit
    end_idx = start_idx + limit

    paginated_data = filtered.iloc[start_idx:end_idx]

    results = [
        map_row_to_transaction(row)
        for _, row in paginated_data.iterrows()
    ]

    return {
        "page": page,
        "total_pages": total_pages,
        "total_items": total_items,
        "transactions": results,
    }


def get_transaction_types():
    """Liste les types de transactions uniques."""
    df = get_data()
    if df.empty or "use_chip" not in df.columns:
        return []
    return df["use_chip"].dropna().unique().tolist()


def get_recent_transactions(n: int):
    """Récupère les N dernières transactions."""
    df = get_data()
    if df.empty:
        return []
    recent_df = df.tail(n).iloc[::-1]
    return [map_row_to_transaction(row) for _, row in recent_df.iterrows()]


def get_transactions_by_customer(customer_id: int):
    df = get_data()

    if df.empty or "client_id" not in df.columns:
        return []

    customer_df = df[df["client_id"].astype(str) == str(customer_id)]

    return [
        map_row_to_transaction(row)
        for _, row in customer_df.head(50).iterrows()
    ]


def get_transactions_to_merchant(merchant_id: int):
    df = get_data()

    if df.empty or "merchant_id" not in df.columns:
        return []

    merchant_df = df[df["merchant_id"].astype(str) == str(merchant_id)]

    return [
        map_row_to_transaction(row)
        for _, row in merchant_df.head(50).iterrows()
    ]

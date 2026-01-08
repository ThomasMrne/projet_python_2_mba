import math
from typing import Dict, Any, Optional
import pandas as pd
from src.banking_api.services.data_loader import get_data


def map_row_to_transaction(row) -> Dict[str, Any]:
    """Helper pour transformer une ligne Pandas en dictionnaire propre"""
    item = row.to_dict()
    item["id"] = str(item["id"])
    item["type"] = str(item.get("use_chip", "Unknown"))
    item["nameOrig"] = f"Client_{item.get('client_id', '0')}"
    item["nameDest"] = f"Merchant_{item.get('merchant_id', '0')}"

    raw_amount = float(item.get("amount", 0.0))
    item["amount"] = abs(raw_amount)
    item["formatted_amount"] = f"${abs(raw_amount):,.2f}"

    # Nettoyage
    if item.get("merchant_state") == 0 or pd.isna(item.get("merchant_state")):
        item["merchant_state"] = None
    if item.get("errors") == 0 or pd.isna(item.get("errors")):
        item["errors"] = None
    if pd.isna(item.get("zip")):
        item["zip"] = None
    if pd.isna(item.get("mcc")):
        item["mcc"] = None

    return item


def get_transactions(
    page: int,
    limit: int,
    type: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
):
    df = get_data()
    if df.empty:
        return {"page": page, "total_pages": 0, "total_items": 0, "transactions": []}

    filtered = df
    if type:
        filtered = filtered[filtered["use_chip"] == type]
    if min_amount is not None:
        filtered = filtered[filtered["amount"].abs() >= min_amount]
    if max_amount is not None:
        filtered = filtered[filtered["amount"].abs() <= max_amount]

    total_items = len(filtered)
    total_pages = math.ceil(total_items / limit)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit

    paginated_data = filtered.iloc[start_idx:end_idx]
    results = [map_row_to_transaction(row) for _, row in paginated_data.iterrows()]

    return {
        "page": page,
        "total_pages": total_pages,
        "total_items": total_items,
        "transactions": results,
    }


def get_transaction_types():
    df = get_data()
    if df.empty or "use_chip" not in df.columns:
        return []
    return df["use_chip"].dropna().unique().tolist()


def get_recent_transactions(n: int):
    df = get_data()
    if df.empty:
        return []
    recent_df = df.tail(n).iloc[::-1]
    return [map_row_to_transaction(row) for _, row in recent_df.iterrows()]


def get_transactions_by_customer(customer_id: int):
    df = get_data()
    customer_df = df[df["client_id"] == customer_id]
    return [map_row_to_transaction(row) for _, row in customer_df.head(50).iterrows()]


def get_transactions_to_merchant(merchant_id: int):
    df = get_data()
    merchant_df = df[df["merchant_id"] == merchant_id]
    return [map_row_to_transaction(row) for _, row in merchant_df.head(50).iterrows()]


def get_transaction_by_id(search_id: int):
    df = get_data()
    row = df[df["id"] == search_id]
    if row.empty:
        return None
    return map_row_to_transaction(row.iloc[0])

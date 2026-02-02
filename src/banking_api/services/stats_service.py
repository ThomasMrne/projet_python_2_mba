from src.banking_api.services.data_loader import get_data


def get_global_stats():
    df = get_data()

    if df.empty:
        return {
            "total_transactions": 0,
            "average_amount": 0.0,
            "top_transaction": None,
            "fraud_rate": 0.0,
            "most_common_type": None
        }

    total_tx = len(df)

    avg_amount = 0.0
    if "amount" in df.columns:
        avg_amount = df["amount"].abs().mean()

    top_tx = None
    if "amount" in df.columns:
        max_idx = df["amount"].abs().idxmax()
        row = df.loc[max_idx]
        top_tx = {
            "id": str(row.get("id", "Unknown")),
            "amount": float(abs(row.get("amount", 0.0))),
            "date": str(row.get("date", ""))
        }

    return {
        "total_transactions": total_tx,
        "average_amount": round(avg_amount, 2),
        "top_transaction": top_tx,
        "fraud_rate": 0.0,
        "most_common_type": "Payment"
    }


def get_amount_distribution():
    return {
        "bins": ["0-50", "50-100", "100+"],
        "counts": [10, 5, 2]
    }


def get_transactions_by_type():
    """Compte les transactions par type."""
    df = get_data()
    if df.empty:
        return []

    if "type" in df.columns:
        counts = df["type"].value_counts()
    elif "use_chip" in df.columns:
        counts = df["use_chip"].value_counts()
    else:
        return []

    return [
        {"type": str(t), "count": int(c)}
        for t, c in counts.items()
    ]


def get_daily_transaction_volume():
    """Volume quotidien des transactions."""
    df = get_data()
    if df.empty or "date" not in df.columns:
        return []

    try:
        dates_series = df["date"].astype(str).str[:10]
        daily_counts = dates_series.value_counts().sort_index()

        return [
            {"date": str(d), "count": int(c)}
            for d, c in daily_counts.items()
        ]
    except Exception:
        return []

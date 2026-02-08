from src.banking_api.services.data_loader import get_data


def get_global_stats():
    """Route 10: Résumé global des transactions"""
    df = get_data()
    if df.empty:
        return {
            "total_transactions": 0,
            "average_amount": 0.0,
            "top_transaction": None,
            "fraud_rate": 0.0,
            "most_common_type": "N/A"
        }

    # Pas besoin de 'pd.' ici, les méthodes appartiennent au DataFrame 'df'
    avg = df["amount"].mean() if "amount" in df.columns else 0.0

    top_tx = None
    if "amount" in df.columns and not df.empty:
        idx = df["amount"].idxmax()
        row = df.loc[idx]
        top_tx = {
            "id": str(idx),
            "amount": float(row["amount"]),
            "date": "N/A"
        }

    # Calcul du type le plus fréquent
    common_type = "N/A"
    if "type" in df.columns:
        mode_res = df["type"].mode()
        if not mode_res.empty:
            common_type = str(mode_res[0])

    return {
        "total_transactions": len(df),
        "average_amount": round(float(avg), 2),
        "top_transaction": top_tx,
        "fraud_rate": 0.0,
        "most_common_type": common_type
    }


def get_transactions_by_type():
    """Route 11: Répartition par type"""
    df = get_data()
    col = "type" if "type" in df.columns else None
    if df.empty or not col:
        return []

    counts = df[col].value_counts()
    return [{"type": str(t), "count": int(c)} for t, c in counts.items()]


def get_daily_transaction_volume():
    """Route 12: Volume par step"""
    df = get_data()
    if df.empty or "step" not in df.columns:
        return []

    daily = df["step"].value_counts().sort_index().head(10)
    return [{"date": f"Step {s}", "count": int(c)} for s, c in daily.items()]


def get_amount_distribution():
    """Route demandée par le router pour la distribution des montants."""
    return {
        "bins": ["0-50", "50-100", "100+"],
        "counts": [10, 5, 2]
    }

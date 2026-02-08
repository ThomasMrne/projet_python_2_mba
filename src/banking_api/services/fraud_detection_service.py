from src.banking_api.services.data_loader import get_data


def get_fraud_summary():
    df = get_data()
    if df.empty:
        return {"total_frauds": 0, "flagged_by_system": 0, "fraud_rate": 0.0}

    col = "isFraud" if "isFraud" in df.columns else "errors"
    # Filtrage robuste (gère string, int, float)
    frauds = df[df[col].astype(str).isin(["1", "1.0", "True"])]
    total = len(frauds)
    rate = total / len(df) if len(df) > 0 else 0.0

    return {
        "total_frauds": total,
        "flagged_by_system": total,
        "fraud_rate": float(round(rate, 5))
    }


def get_fraud_by_type():
    df = get_data()
    f_col = "isFraud" if "isFraud" in df.columns else "errors"
    t_col = "type" if "type" in df.columns else "use_chip"

    if df.empty or f_col not in df.columns:
        return []

    frauds = df[df[f_col].astype(str).isin(["1", "1.0", "True"])]
    if frauds.empty:
        return []

    stats = frauds.groupby(t_col).size().reset_index(name="count")
    return stats.rename(columns={t_col: "type"}).to_dict(orient="records")


def predict_fraud(amount: float, tx_type: str):
    prob = 0.1
    if amount > 1000:
        prob += 0.5
    if any(x in tx_type.upper() for x in ["TRANSFER", "CASH_OUT"]):
        prob += 0.3

    prob = min(prob, 0.99)
    is_f = prob > 0.7
    return {
        "isFraud": is_f,
        "probability": float(round(prob, 2)),
        "risk_level": "High" if is_f else "Low"
    }

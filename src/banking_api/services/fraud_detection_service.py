from src.banking_api.services.data_loader import get_data


def get_fraud_summary():
    """Route 13: Calcule les indicateurs globaux de fraude sur le dataset."""
    df = get_data()
    if df.empty:
        return {"total_frauds": 0, "flagged_by_system": 0, "fraud_rate": 0.0}

    # Sélection de la colonne de fraude selon le dataset (isFraud ou errors)
    col = "isFraud" if "isFraud" in df.columns else "errors"
    if col not in df.columns:
        return {"total_frauds": 0, "flagged_by_system": 0, "fraud_rate": 0.0}

    # Filtrage robuste pour identifier les lignes marquées comme frauduleuses
    frauds = df[df[col].astype(str).isin(["1", "1.0", "True"])]
    total = len(frauds)
    rate = total / len(df) if len(df) > 0 else 0.0

    return {
        "total_frauds": total,
        "flagged_by_system": total,
        "fraud_rate": float(round(rate, 5))
    }


def get_fraud_by_type():
    """Route 14: Analyse la répartition des fraudes par type de transaction."""
    df = get_data()
    f_col = "isFraud" if "isFraud" in df.columns else "errors"
    t_col = "type" if "type" in df.columns else "use_chip"

    # Vérification de la présence des colonnes nécessaires à l'analyse
    if df.empty or f_col not in df.columns or t_col not in df.columns:
        return []
    # Extraction des lignes frauduleuses uniquement
    frauds = df[df[f_col].astype(str).isin(["1", "1.0", "True"])]
    if frauds.empty:
        return []
    # Groupement par type pour compter les occurrences de fraude
    stats = frauds.groupby(t_col).size().reset_index(name="count")
    return stats.rename(columns={t_col: "type"}).to_dict(orient="records")


def predict_fraud(amount: float, tx_type: str, old_bal:
                  float = 0, new_bal: float = 0):
    """
    Algorithme de détection de risque basé sur des règles.
    Prend en compte l'évolution du solde du compte.
    """
    prob = 0.1

    # Risque élevé pour les transactions dépassant 1000 unités
    if amount > 1000:
        prob += 0.5

    # Les types TRANSFER et CASH_OUT sont statistiquement plus risqués
    if any(x in tx_type.upper() for x in ["TRANSFER", "CASH_OUT"]):
        prob += 0.3

    # LOGIQUE AJOUTÉE : Détection d'un vidage de compte (solde tombe à 0)
    if old_bal > 0 and new_bal == 0 and amount > 0:
        prob += 0.2

    # Plafonnement de la probabilité à 99%
    prob = min(prob, 0.99)
    is_f = prob > 0.7

    return {
        "isFraud": is_f,
        "probability": float(round(prob, 2)),
        "risk_level": "High" if is_f else "Low"
    }

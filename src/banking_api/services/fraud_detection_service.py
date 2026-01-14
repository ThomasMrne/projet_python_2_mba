from src.banking_api.services.data_loader import get_data


def get_fraud_summary():
    """Route 13: Vue d'ensemble de la fraude (Basé sur les erreurs)"""
    df = get_data()
    if df.empty:
        return {
            "total_frauds": 0,
            "flagged_by_system": 0,
            "fraud_rate": 0.0
        }

    total_frauds = 0

    if "errors" in df.columns:
        # Création d'un masque propre pour éviter les lignes trop longues
        # et les problèmes d'indentation (E122/E501)
        mask = (
            (df["errors"] != 0)
            & (df["errors"] != "0")
            & (df["errors"].notna())
        )
        fraud_df = df[mask]
        total_frauds = len(fraud_df)

    # Calcul du taux avec gestion de la division par zéro
    fraud_rate = 0.0
    if len(df) > 0:
        fraud_rate = total_frauds / len(df)

    return {
        "total_frauds": total_frauds,
        "flagged_by_system": total_frauds,
        "fraud_rate": float(round(fraud_rate, 5)),
    }


def get_fraud_by_type():
    """Route 14: Répartition de la fraude par type de transaction"""
    df = get_data()
    required_cols = ["errors", "use_chip"]

    # Vérification de sécurité
    if df.empty or any(col not in df.columns for col in required_cols):
        return []

    # Même technique du masque pour filtrer proprement
    mask = (
        (df["errors"] != 0)
        & (df["errors"] != "0")
        & (df["errors"].notna())
    )
    frauds = df[mask]

    if frauds.empty:
        return []

    # Groupby aligné verticalement pour la lisibilité
    stats = (
        frauds.groupby("use_chip")
        .size()
        .reset_index(name="count")
    )
    stats = stats.rename(columns={"use_chip": "type"})

    return stats.to_dict(orient="records")


def predict_fraud(amount: float, type: str):
    """
    Route 15: Simulation de scoring (Prédiction).
    Règle arbitraire simple pour l'exercice.
    """
    probability = 0.1  # Risque de base

    # Règle 1 : Gros montant
    if amount > 1000:
        probability += 0.5

    # Règle 2 : Transaction en ligne (souvent plus risquée)
    if "Online" in type:
        probability += 0.3

    # Plafond à 1.0 (100%)
    probability = min(probability, 0.99)

    is_fraud = probability > 0.7

    return {
        "isFraud": is_fraud,
        "probability": float(round(probability, 2)),
        "risk_level": "High" if is_fraud else "Low",
    }

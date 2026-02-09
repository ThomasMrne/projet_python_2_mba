import pandas as pd
from src.banking_api.services.data_loader import get_data


def get_global_stats():
    """Route 10: Résumé global des transactions avec calcul dynamique."""
    df = get_data()
    # Gestion du cas où le dataset est vide au démarrage
    if df.empty:
        return {
            "total_transactions": 0,
            "average_amount": 0.0,
            "top_transaction": None,
            "fraud_rate": 0.0,
            "most_common_type": "N/A"
        }

    # Calcul de la moyenne des montants
    avg = df["amount"].mean() if "amount" in df.columns else 0.0

    # --- CALCUL DYNAMIQUE DU TAUX DE FRAUDE ---
    fraud_rate = 0.0
    if "isFraud" in df.columns and not df.empty:
        total_frauds = df["isFraud"].astype(float).sum()
        fraud_rate = round(float(total_frauds / len(df)), 5)

    # Identification de la transaction ayant le montant record
    top_tx = None
    if "amount" in df.columns and not df.empty:
        idx = df["amount"].idxmax()
        row = df.loc[idx]
        top_tx = {
            "id": str(idx),
            "amount": float(row["amount"]),
            "date": "N/A"
        }

    # Détermination de la catégorie de transaction la plus représentée
    common_type = "N/A"
    if "type" in df.columns:
        mode_res = df["type"].mode()
        if not mode_res.empty:
            common_type = str(mode_res[0])

    return {
        "total_transactions": len(df),
        "average_amount": round(float(avg), 2),
        "top_transaction": top_tx,
        "fraud_rate": fraud_rate,
        "most_common_type": common_type
    }


def get_transactions_by_type():
    """Route 11: Répartition par type de mouvement"""
    df = get_data()
    col = "type" if "type" in df.columns else None
    if df.empty or not col:
        return []

    counts = df[col].value_counts()
    return [{"type": str(t), "count": int(c)} for t, c in counts.items()]


def get_daily_transaction_volume():
    """Route 12: Analyse du volume d'activité par unité de temps (Step)."""
    df = get_data()
    if df.empty or "step" not in df.columns:
        return []

    # Analyse des 10 premières unités temporelles du dataset
    daily = df["step"].value_counts().sort_index().head(10)
    return [{"date": f"Step {s}", "count": int(c)} for s, c in daily.items()]


def get_amount_distribution():
    """
    Route 13: Répartition des montants par tranches (Histogramme).
    Utilise pd.cut pour segmenter les 13M de lignes efficacement.
    """
    df = get_data()
    bins_labels = ["0-50", "50-100", "100+"]

    if df.empty or "amount" not in df.columns:
        return {
            "bins": bins_labels,
            "counts": [0, 0, 0]
        }

# Définition des bornes des tranches monétaires (jusqu'à l'infini)
    bins_edges = [0, 50, 100, float('inf')]

    # Segmentation automatique des données dans les catégories définies
    segments = pd.cut(
        df["amount"],
        bins=bins_edges,
        labels=bins_labels,
        right=False
    )

    # Comptage par tranche avec garantie de l'ordre d'affichage
    counts = segments.value_counts().reindex(bins_labels, fill_value=0)

    return {
        "bins": bins_labels,
        "counts": [int(c) for c in counts.values]
    }

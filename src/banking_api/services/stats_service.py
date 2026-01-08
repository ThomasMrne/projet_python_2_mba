import pandas as pd
from src.banking_api.services.data_loader import get_data


def get_global_stats():
    """
    Route 9: Version corrigée pour un taux de fraude réaliste.
    """
    df = get_data()
    if df.empty:
        return {
            "total_transactions": 0,
            "fraud_rate": 0.0,
            "avg_amount": 0.0,
            "most_common_type": "N/A",
        }

    total_transactions = len(df)

    # Correction Fraude : On ne compte que si 'errors' n'est ni 0, ni vide, ni "0"
    if "errors" in df.columns:
        # On filtre pour garder uniquement les vraies erreurs (texte)
        fraud_df = df[
            (df["errors"] != 0) & (df["errors"] != "0") & (df["errors"].notna())
        ]
        fraud_count = len(fraud_df)
    else:
        fraud_count = 0

    fraud_rate = fraud_count / total_transactions if total_transactions > 0 else 0
    avg_amount = df["amount"].abs().mean()

    most_common_type = "N/A"
    if "use_chip" in df.columns:
        try:
            most_common_type = df["use_chip"].mode()[0]
        except Exception:
            pass

    return {
        "total_transactions": int(total_transactions),
        "fraud_rate": float(
            round(fraud_rate, 5)
        ),  # Sera maintenant proche de 0, ce qui est normal
        "avg_amount": float(round(avg_amount, 2)),
        "most_common_type": str(most_common_type),
    }


def get_amount_distribution():
    """
    Route 10: Histogramme des montants.
    """
    df = get_data()
    if df.empty:
        return {"bins": [], "counts": []}

    amounts = df["amount"].abs()
    bins = [0, 50, 100, 500, 1000, float("inf")]
    labels = ["0-50", "50-100", "100-500", "500-1000", "1000+"]

    try:
        binned = pd.cut(amounts, bins=bins, labels=labels, right=False)
        counts = binned.value_counts().sort_index()

        return {"bins": counts.index.tolist(), "counts": counts.values.tolist()}
    except Exception as e:
        print(f"Erreur stats distribution: {e}")
        return {"bins": [], "counts": []}


def get_stats_by_type():
    """
    Route 11: Stats par type.
    """
    df = get_data()
    if df.empty or "use_chip" not in df.columns:
        return []

    stats = (
        df.groupby("use_chip")
        .agg(count=("amount", "count"), avg_amount=("amount", "mean"))
        .reset_index()
    )

    stats["avg_amount"] = stats["avg_amount"].abs()
    stats = stats.rename(columns={"use_chip": "type"})

    return stats.to_dict(orient="records")


def get_daily_stats():
    """
    Route 12: Tendance annuelle.
    """
    df = get_data()
    if df.empty or "date" not in df.columns:
        return []

    try:
        # Extraction de l'année
        df["year"] = df["date"].astype(str).str[:4]

        daily = (
            df.groupby("year")
            .agg(count=("amount", "count"), avg_amount=("amount", "mean"))
            .reset_index()
            .sort_values("year")
        )

        daily["avg_amount"] = daily["avg_amount"].abs()

        result = []
        for _, row in daily.iterrows():
            # Sécurisation si l'année n'est pas un chiffre
            year_val = row["year"]
            step_val = int(year_val) if year_val.isdigit() else 0

            result.append(
                {
                    "step": step_val,
                    "count": int(row["count"]),
                    "avg_amount": float(row["avg_amount"]),
                }
            )

        return result

    except Exception as e:
        print(f"Erreur stats daily: {e}")
        return []

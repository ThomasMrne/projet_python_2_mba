import pandas as pd
from pathlib import Path

# Variable globale
global_dataframe = None


def clean_currency_col(df, col):
    """Fonction aide pour nettoyer une colonne monétaire."""
    if col not in df.columns or df[col].dtype != "object":
        return

    # On nettoie en plusieurs étapes courtes
    series = df[col].astype(str)
    series = series.str.replace("$", "", regex=False)
    series = series.str.replace(",", "", regex=False)
    df[col] = pd.to_numeric(series, errors="coerce")


def load_dataset():
    """
    Charge le fichier CSV et nettoie les symboles monétaires.
    """
    global global_dataframe

    base_path = Path(__file__).resolve().parents[3]
    csv_path = base_path / "data" / "transactions.csv"

    print(f"Chargement : {csv_path}")

    if not csv_path.exists():
        print("ERREUR : csv introuvable !")
        return False

    try:
        # 1. Chargement
        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.strip()

        # 2. Nettoyage
        target_cols = [
            "amount",
            "oldbalanceOrg",
            "newbalanceOrig",
            "oldbalanceDest",
            "newbalanceDest",
        ]

        for col in target_cols:
            clean_currency_col(df, col)

        df.fillna(0, inplace=True)
        global_dataframe = df

        count = len(df)
        print(f"Succès ! {count} transactions chargées.")
        return True

    except Exception as e:
        print(f"Erreur lecture CSV : {e}")
        return False


def get_data() -> pd.DataFrame:
    if global_dataframe is None:
        return pd.DataFrame()
    return global_dataframe

import pandas as pd
from pathlib import Path

global_dataframe = None


def clean_currency_col(df, col):
    """Nettoie une colonne monétaire."""
    if col not in df.columns or df[col].dtype != "object":
        return
    s = df[col].astype(str).str.replace("$", "", regex=False)
    s = s.str.replace(",", "", regex=False)
    df[col] = pd.to_numeric(s, errors="coerce")


def load_dataset():
    """Charge le dataset via recherche multi-chemins."""
    global global_dataframe
    paths = [
        Path(__file__).resolve().parents[3] / "data" / "transactions.csv",
        Path.cwd() / "data" / "transactions.csv",
        Path.cwd() / "src" / "banking_api" / "data" / "transactions.csv"
    ]
    t_path = next((p for p in paths if p.exists()), None)
    if not t_path:
        return False
    try:
        df = pd.read_csv(t_path)
        df.columns = df.columns.str.strip()
        cols = [
            "amount", "oldbalanceOrg", "newbalanceOrig",
            "oldbalanceDest", "newbalanceDest"
        ]
        for col in cols:
            clean_currency_col(df, col)
        df.fillna(0, inplace=True)
        global_dataframe = df
        return True
    except Exception as e:
        print(f"Erreur lors du chargement du dataset: {e}")
        return False


def get_data() -> pd.DataFrame:
    """Renvoie le dataframe chargé."""
    return global_dataframe if global_dataframe is not None else pd.DataFrame()

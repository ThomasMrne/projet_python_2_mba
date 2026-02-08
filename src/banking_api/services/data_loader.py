import pandas as pd
from pathlib import Path

global_dataframe = pd.DataFrame()


def clean_currency_col(df, col):
    """Nettoie une colonne monétaire en gérant les types mixtes."""
    if col not in df.columns:
        return
    # On convertit tout en string, puis on nettoie les symboles
    s = df[col].astype(str).str.replace("$", "", regex=False)
    s = s.str.replace(",", "", regex=False)
    df[col] = pd.to_numeric(s, errors="coerce")


def load_dataset():
    """Charge le dataset avec une tolérance totale aux types de données."""
    global global_dataframe
    p = Path("/Users/thomasmarie-anne/Desktop/Bureau - MacBook Air de Thomas/"
             "projet_python_2_mba/data/transactions.csv")
    try:
        # Cela accepte les '0' au milieu des noms sans planter.
        df = pd.read_csv(p, low_memory=False, dtype=object)

        df.columns = df.columns.str.strip()

        numeric_cols = [
            "amount", "oldbalanceOrg", "newbalanceOrig",
            "oldbalanceDest", "newbalanceDest"
        ]
        for col in numeric_cols:
            clean_currency_col(df, col)

        # Conversion explicite des labels de fraude si présents
        for col in ["isFraud", "isFlaggedFraud"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        df.fillna(0, inplace=True)
        global_dataframe = df
        print(f"--- SUCCÈS : {len(df)} LIGNES CHARGÉES ---")
        return True
    except Exception as e:
        print(f"Erreur lors du chargement du dataset: {e}")
        return False


def get_data() -> pd.DataFrame:
    """Renvoie le dataframe chargé."""
    return global_dataframe

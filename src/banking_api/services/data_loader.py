import pandas as pd
from pathlib import Path

# Variable globale
global_dataframe = None


def load_dataset():
    """
    Charge le fichier CSV et nettoie les symboles monétaires ($).
    """
    global global_dataframe

    base_path = Path(__file__).resolve().parents[3]
    data_path = base_path / "data" / "transactions.csv"

    print(f"Chargement des données depuis : {data_path}")

    if not data_path.exists():
        print("ERREUR : Le fichier transactions.csv est introuvable !")
        return False

    try:
        # 1. Chargement
        df = pd.read_csv(data_path)

        # Nettoyage des noms de colonnes
        df.columns = df.columns.str.strip()

        # 2. NETTOYAGE DES DEVISES ($) - C'est ici que ça bloquait
        # Liste des colonnes qui contiennent de l'argent
        money_cols = [
            "amount",
            "oldbalanceOrg",
            "newbalanceOrig",
            "oldbalanceDest",
            "newbalanceDest",
        ]

        for col in money_cols:
            if col in df.columns:
                # Si la colonne est considérée comme du texte (object), on la nettoie
                if df[col].dtype == "object":
                    # On remplace le $ et les virgules éventuelles
                    df[col] = df[col].astype(str).str.replace("$", "", regex=False)
                    df[col] = df[col].str.replace(",", "", regex=False)
                    # On convertit en nombre
                    df[col] = pd.to_numeric(df[col], errors="coerce")

        # 3. Remplacer les cases vides par 0
        df.fillna(0, inplace=True)

        global_dataframe = df
        print(
            f"Succès ! {len(global_dataframe)} transactions chargées et nettoyées ($ retirés)."
        )
        return True

    except Exception as e:
        print(f"Erreur GRAVE lors de la lecture du CSV : {e}")
        return False


def get_data() -> pd.DataFrame:
    if global_dataframe is None:
        return pd.DataFrame()
    return global_dataframe

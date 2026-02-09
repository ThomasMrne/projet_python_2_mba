import pandas as pd
import numpy as np
import os
from pathlib import Path

# Variable globale pour stocker les données en mémoire vive (RAM)
global_dataframe = pd.DataFrame()


def clean_currency_col(df, col):
    """Nettoie une colonne monétaire en retirant les symboles parasites."""
    if col not in df.columns:
        return
    # Transforme tout en texte pour supprimer les $ et les virgules
    s = df[col].astype(str).str.replace("$", "", regex=False)
    s = s.str.replace(",", "", regex=False)
    # Conversion finale en nombre (float)
    df[col] = pd.to_numeric(s, errors="coerce")


def load_dataset():
    """Charge le dataset avec un typage strict pour les calculs."""
    global global_dataframe

    # Détermination dynamique du chemin du fichier CSV
    root = Path(__file__).resolve().parents[3]
    default_path = root / "data" / "transactions.csv"

    # Chemin portable via variable d'environnement ou chemin relatif
    p = Path(os.environ.get("DATASET_PATH", str(default_path)))

    try:
        # Lecture initiale
        df = pd.read_csv(p, low_memory=False, dtype=object)
        df.columns = df.columns.str.strip()

        # 1. Conversion des colonnes monétaires
        numeric_cols = [
            "amount", "oldbalanceOrg", "newbalanceOrig",
            "oldbalanceDest", "newbalanceDest"
        ]
        for col in numeric_cols:
            clean_currency_col(df, col)

        # 2. Conversion des indicateurs de fraude en nombres (0 ou 1)
        for col in ["isFraud", "isFlaggedFraud"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # 3. Traitement intelligent des valeurs manquantes (NaN)
        # On remplit les nombres avec 0.0 pour ne pas casser les calculs
        num_cols = df.select_dtypes(include=[np.number]).columns
        df[num_cols] = df[num_cols].fillna(0.0)

        # On remplit le texte avec des chaînes vides pour la clarté
        obj_cols = df.select_dtypes(exclude=[np.number]).columns
        df[obj_cols] = df[obj_cols].fillna("")

        global_dataframe = df
        print(f"--- SUCCÈS : {len(df)} LIGNES CHARGÉES ---")
        return True
    except Exception as e:
        print(f"Erreur lors du chargement du dataset: {e}")
        return False


def get_data() -> pd.DataFrame:
    """Fournit l'accès aux données chargées aux autres services."""
    return global_dataframe

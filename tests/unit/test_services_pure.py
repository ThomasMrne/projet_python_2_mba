from src.banking_api.services.transactions_service import (
    map_row_to_transaction
)
import pandas as pd
import numpy as np


def test_map_row_cleanup():
    """Vérifie que la fonction de mapping nettoie correctement les données."""
    # Création d'une ligne de données "sale" avec des valeurs problématiques
    dirty_row = pd.Series({
        "id": 123,
        "amount": 50.0,
        "merchant_state": np.nan,
        "errors": "0"
    })

    # Appel de la logique de transformation
    result = map_row_to_transaction(dirty_row)

    # Vérifications:
    # 1. Le NaN doit être converti en None (standard JSON)
    assert result["merchant_state"] is None

    # 2. Le "0" des erreurs doit être interprété comme une absence d'erreur
    assert result["errors"] is None

    # 3. L'ID doit être systématiquement converti en chaîne de caractères
    assert result["id"] == "123"

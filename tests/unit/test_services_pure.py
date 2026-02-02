from src.banking_api.services.transactions_service import (
    map_row_to_transaction
)
import pandas as pd
import numpy as np


def test_map_row_cleanup():
    dirty_row = pd.Series({
        "id": 123,
        "amount": 50.0,
        "merchant_state": np.nan,
        "errors": "0"
    })

    result = map_row_to_transaction(dirty_row)

    assert result["merchant_state"] is None
    assert result["errors"] is None
    assert result["id"] == "123"

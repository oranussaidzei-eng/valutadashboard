# Tests for analysis.py


import pandas as pd

from currency_dashboard.analysis import create_dataframe


def test_create_dataframe():
    historical_data = {
        "2026-01-01": 1.50,
        "2026-01-02": 1.55,
        "2026-01-03": 1.60,
    }

    df = create_dataframe(historical_data)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert "date" in df.columns
    assert "rate" in df.columns


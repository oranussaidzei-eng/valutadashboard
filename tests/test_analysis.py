# Tests for analysis.py


import pandas as pd

from currency_dashboard.analysis import create_dataframe, percentage_change
from currency_dashboard.analysis import (
    create_dataframe,
    percentage_change,
    monthly_average,
)

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



def test_percentage_change():
    start_rate = 1.50
    end_rate = 1.65

    result = percentage_change(start_rate, end_rate)

    assert result == 10.0


def test_monthly_average():
    historical_data = {
        "2026-01-01": 1.50,
        "2026-01-15": 1.60,
        "2026-02-01": 1.70,
        "2026-02-15": 1.80,

    }

    df= create_dataframe(historical_data)
    result = monthly_average(df)

    assert result.loc["2026-01"] == 1.55
    assert result.loc["2026-02"] == 1.75

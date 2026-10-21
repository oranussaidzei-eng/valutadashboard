import pandas as pd

def create_dataframe(historical_data):
    df = pd.DataFrame(
        list(historical_data.items()),
        columns=["date", "rate"]
    )

    return df 
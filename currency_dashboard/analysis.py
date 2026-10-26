import pandas as pd

def create_dataframe(historical_data):
    df = pd.DataFrame(
        list(historical_data.items()),
        columns=["date", "rate"]
    )

    return df 



def percentage_change(start_rate, end_rate):
    change = ((end_rate - start_rate) / start_rate) * 100
    return round(change, 2)

def monthly_average(df):
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)

    monthly = df.groupby("month")["rate"].mean()

    return monthly

def highest_and_lowest_rate(df):
    highest = df["rate"].max()
    lowest = df["rate"].min()

    return highest, lowest
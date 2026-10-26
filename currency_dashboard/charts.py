import plotly.express as px


def create_history_chart(df):
    fig = px.line(
        df,
        x="date",
        y="rate",
        title="Exchange Rate History"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Exchange Rate"
    )

    return fig.to_html(full_html=False)

def create_monthly_average_chart(monthly_data):
    fig = px.bar(
        x=monthly_data.index,
        y=monthly_data.values,
        title="Monthly Average Exchange Rate",
        labels={
            "x": "Month",
            "y": "Average Exchange Rate"
        }
    )

    return fig.to_html(full_html=False)

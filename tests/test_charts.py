import pandas as pd

from currency_dashboard.charts import (
    create_history_chart,
    create_monthly_average_chart,
)


def test_create_history_chart():
    # Create sample data for the test
    df = pd.DataFrame(
        {
            "date": [
                "2026-10-01",
                "2026-10-02",
                "2026-10-03",
            ],
            "rate": [0.091, 0.092, 0.093],
        }
    )

    # Generate the chart
    chart = create_history_chart(df)

    # Check that Plotly returns HTML
    assert isinstance(chart, str)
    assert "Plotly.newPlot" in chart

    # Check that the correct chart labels are included
    assert "Exchange Rate" in chart
    assert "Date" in chart

    # Check the navy chart color
    assert "#172B45" in chart


def test_create_monthly_average_chart():
    # Create monthly averages for the test
    monthly_data = pd.Series(
        [0.091, 0.092, 0.093],
        index=["July", "August", "September"],
    )

    # Generate the chart
    chart = create_monthly_average_chart(monthly_data)

    # Check that Plotly returns HTML
    assert isinstance(chart, str)
    assert "Plotly.newPlot" in chart

    # Check that the correct labels are included
    assert "Average Exchange Rate" in chart
    assert "Month" in chart

    # Check the navy chart color
    assert "#172B45" in chart

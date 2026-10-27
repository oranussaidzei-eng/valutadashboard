import pandas as pd

from flask import Flask, render_template, request

from currency_dashboard.analysis import monthly_average
from currency_dashboard.charts import (
    create_history_chart,
    create_monthly_average_chart,
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        from_currency = request.form["from_currency"]
        to_currency = request.form["to_currency"]
        amount = request.form["amount"]

        return render_template(
            "home.html",
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount,
            show_result=True
        )

    return render_template("home.html")


@app.route("/history")
def history():
    from_currency = request.args.get("from", "SEK")
    to_currency = request.args.get("to", "EUR")

    data = {
        "date": [
            "2026-01-01",
            "2026-01-15",
            "2026-02-01",
            "2026-02-15",
            "2026-03-01",
            "2026-03-15"
        ],
        "rate": [
            10.20,
            10.35,
            10.28,
            10.42,
            10.50,
            10.45
        ]
    }

    df = pd.DataFrame(data)

    chart = create_history_chart(df)

    monthly_data = monthly_average(df)
    monthly_chart = create_monthly_average_chart(monthly_data)

    return render_template(
        "history.html",
        chart=chart,
        monthly_chart=monthly_chart,
        from_currency=from_currency,
        to_currency=to_currency
    )


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
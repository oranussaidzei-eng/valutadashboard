from datetime import date, timedelta

import pandas as pd
from flask import Flask, render_template, request

from currency_dashboard.analysis import (
    create_dataframe,
    highest_and_lowest_rate,
    monthly_average,
    percentage_change,
)
from currency_dashboard.charts import (
    create_history_chart,
    create_monthly_average_chart,
)
from currency_dashboard.currency_api import hämta_tidsserie, hämta_valutakurs

app = Flask(__name__)

CURRENCIES = ["SEK", "USD", "EUR", "TND", "AFN", "CDF"]


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")

    from_currency = request.form.get("from_currency")
    to_currency = request.form.get("to_currency")
    amount = request.form.get("amount")

    if from_currency not in CURRENCIES or to_currency not in CURRENCIES:
        return render_template("error.html", fel="Välj giltiga valutor"), 400

    try:
        amount_value = float(amount)

        if not pd.notna(amount_value) or amount_value <= 0:
            raise ValueError

    except (ValueError, TypeError):
        return render_template(
            "error.html", fel="Ange ett giltigt belopp större än noll."
        ), 400

    try:
        if from_currency == to_currency:
            rate = 1.0
        else:
            api_result = hämta_valutakurs(from_currency, to_currency)

            if isinstance(api_result, (int, float)):
                rate = float(api_result)

            elif isinstance(api_result, dict):
                if "rate" in api_result:
                    rate = float(api_result["rate"])
                elif to_currency in api_result:
                    rate = float(api_result[to_currency])
                else:
                    raise ValueError("Exchange rate not found.")

            else:
                raise ValueError("Unexpected API response.")

        converted_amount = amount_value * rate

    except (ValueError, TypeError, KeyError):
        return render_template(
            "error.html", fel="Valutakursen kunde inte hämtas. Försök igen."
        ), 502

    return render_template(
        "home.html",
        from_currency=from_currency,
        to_currency=to_currency,
        amount=amount,
        converted_amount=converted_amount,
        exchange_rate=rate,
        show_result=True,
    )


@app.route("/history")
def history():
    from_currency = request.args.get("from", "SEK")
    to_currency = request.args.get("to", "EUR")

    if from_currency not in CURRENCIES or to_currency not in CURRENCIES:
        return render_template("error.html", fel="Välj giltiga valutor"), 400

    if from_currency == to_currency:
        return render_template(
            "error.html", fel="Välj två olika valutor för historiken."
        ), 400

    end_date = date.today()
    start_date = end_date - timedelta(days=30)

    historical_data = hämta_tidsserie(
        from_currency,
        to_currency,
        start_date.isoformat(),
        end_date.isoformat(),
    )

    if historical_data is None:
        return render_template(
            "error.html", fel="Historiska kurser kunde inte hämtas. Försök igen."
        ), 502

    if not historical_data:
        return render_template(
            "error.html", fel="Det finns inga valutakurser för perioden."
        ), 502

    try:
        df = create_dataframe(historical_data)

        if df.empty:
            raise ValueError("No historical data available.")

        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")

        highest_rate, lowest_rate = highest_and_lowest_rate(df)

        start_rate = df["rate"].iloc[0]
        current_rate = df["rate"].iloc[-1]
        change = percentage_change(start_rate, current_rate)

        chart = create_history_chart(df)

        monthly_data = monthly_average(df)
        monthly_chart = create_monthly_average_chart(monthly_data)

    except (ValueError, TypeError, KeyError, ZeroDivisionError):
        return render_template(
            "error.html", fel="Historiska data kunde inte bearbetas."
        ), 502

    return render_template(
        "history.html",
        from_currency=from_currency,
        to_currency=to_currency,
        chart=chart,
        monthly_chart=monthly_chart,
        current_rate=current_rate,
        highest_rate=highest_rate,
        lowest_rate=lowest_rate,
        change=change,
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.errorhandler(404)
def saknas(e):
    return render_template("error.html", fel="Sidan finns inte"), 404


if __name__ == "__main__":
    app.run(debug=True)

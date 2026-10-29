
import pandas as pd

from flask import Flask, render_template, request

from currency_api import hämta_valutakurs, hämta_tidsserie

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

# Create the Flask application
app = Flask(__name__)


# Home page and currency converter
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":

        # Get values from the form
        from_currency = request.form.get("from_currency", "SEK")
        to_currency = request.form.get("to_currency", "EUR")
        amount = request.form.get("amount", "")

        # Validate the amount
        try:
            amount_value = float(amount)

            if not pd.notna(amount_value) or amount_value <= 0:
                raise ValueError

        except (ValueError, TypeError):
            return render_template(
                "home.html",
                from_currency=from_currency,
                to_currency=to_currency,
                amount=amount,
                error="Please enter an amount greater than 0.",
            )

        try:
            # Get the exchange rate from Kevin's API
            if from_currency == to_currency:
                rate = 1.0
            else:
                api_result = hämta_valutakurs(
                    from_currency,
                    to_currency
                )

                # Handle numeric or dictionary API responses
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

            # Calculate converted amount
            converted_amount = amount_value * rate

            # Send result to HTML
            return render_template(
                "home.html",
                from_currency=from_currency,
                to_currency=to_currency,
                amount=amount,
                converted_amount=converted_amount,
                exchange_rate=rate,
                show_result=True,
            )

        except Exception:
            return render_template(
                "home.html",
                from_currency=from_currency,
                to_currency=to_currency,
                amount=amount,
                error="Could not fetch the exchange rate. Please try again.",
            )

    return render_template("home.html")


# Historical exchange rate page
@app.route("/history")
def history():

    # Get selected currencies
    from_currency = request.args.get("from", "SEK")
    to_currency = request.args.get("to", "EUR")

    # Use the most recent 30 days
    from datetime import date, timedelta

    end_date = date.today()
    start_date = end_date - timedelta(days=30)

    try:
        # Get historical rates from Kevin's API
        if from_currency == to_currency:
            raise ValueError("Please select two different currencies.")

        historical_data = hämta_tidsserie(
            from_currency,
            to_currency,
            start_date.isoformat(),
            end_date.isoformat(),
        )

        # Convert API data to a DataFrame
        df = create_dataframe(historical_data)

        if df.empty:
            raise ValueError("No historical data available.")

        # Sort data by date
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")

        # Calculate statistics
        highest_rate, lowest_rate = highest_and_lowest_rate(df)

        start_rate = df["rate"].iloc[0]
        current_rate = df["rate"].iloc[-1]

        change = percentage_change(start_rate, current_rate)

        # Create charts
        chart = create_history_chart(df)

        monthly_data = monthly_average(df)
        monthly_chart = create_monthly_average_chart(monthly_data)

        # Send results to HTML
        return render_template(
            "history.html",
            chart=chart,
            monthly_chart=monthly_chart,
            from_currency=from_currency,
            to_currency=to_currency,
            current_rate=current_rate,
            highest_rate=highest_rate,
            lowest_rate=lowest_rate,
            change=change,
        )

    except Exception:
        return render_template(
            "history.html",
            from_currency=from_currency,
            to_currency=to_currency,
            error="Could not load historical rates. Please try again.",
            chart=None,
            monthly_chart=None,
        )


# About page
@app.route("/about")
def about():
    return render_template("about.html")


# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)

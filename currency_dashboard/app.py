# date ger dagens datum och timedelta räknar ut datumet 30 dagar bakåt.
from datetime import date, timedelta

# pandas används kontrollerar saknade tal och omvandlar datumtext till datumvärden.
import pandas as pd

# Flask skapar webbappen, render_template visar HTML-mallarna
# request läser det som skickas till appen.
from flask import Flask, render_template, request

# Analysfunktionerna importers från analysis.py.
# app.py anropar dem och tar emot resultaten.
from currency_dashboard.analysis import (
    create_dataframe,
    highest_and_lowest_rate,
    monthly_average,
    percentage_change,
)

# Diagramfunktionerna retunerar Plotly_diagram som HTML till mallarna.
from currency_dashboard.charts import (
    create_history_chart,
    create_monthly_average_chart,
)

# API-funktionerna hämtar kurser. requests timeout och nätverksfel
# Hanters i currency_api.py
from currency_dashboard.currency_api import hämta_tidsserie, hämta_valutakurs

# Skapar flask-appen.
app = Flask(__name__)

# Detta är valutona som appen tillåter i både formulär och historik.
CURRENCIES = ["SEK", "USD", "EUR", "TND", "AFN", "CDF"]


# Startsidan har två uppgifter: visa formuläret och ta emot dess värden.
# GET används när sidan öppnas, POST när formuläret skickas.
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")

    # Hämtar vilken valuta användaren vill växla från,
    # vilken valuta pengarna ska växlas till och beloppet läses som text.
    from_currency = request.form.get("from_currency")
    to_currency = request.form.get("to_currency")
    amount = request.form.get("amount")

    # Båda valutorna kontrolleras i serverkoden
    if from_currency not in CURRENCIES or to_currency not in CURRENCIES:
        return render_template("error.html", fel="Välj giltiga valutor"), 400

    try:
        # Gör om beloppets text till ett decimaltal
        amount_value = float(amount)

        # Stoppar belopp som är nool, negativa eller saknar ett giltigt talvärde
        # Det skapas då ett ValueError som fångas av except och visar ett felmeddelande.
        if not pd.notna(amount_value) or amount_value <= 0:
            raise ValueError

    except (ValueError, TypeError):
        return render_template(
            "error.html", fel="Ange ett giltigt belopp större än noll."
        ), 400

    try:
        # Om båda valutorna är samma sätts kursen till 1,
        # så beloppet blir ofrändrat utan något API-anrop.
        if from_currency == to_currency:
            rate = 1.0

        else:
            # Valutorna skickas in som argument.
            # Svaret sparas i api_result.
            api_result = hämta_valutakurs(from_currency, to_currency)

            # Om svaret är ett tal sparas det som valutakurs i variabeln rate.
            if isinstance(api_result, (int, float)):
                rate = float(api_result)

            # Om svaret är en dictionary letar koden efter kursen
            elif isinstance(api_result, dict):
                # Hämtar kursen från rate om den finns i svaret.
                if "rate" in api_result:
                    rate = float(api_result["rate"])

                # Annars letar koden efter kursen den valda valutakoden.
                elif to_currency in api_result:
                    rate = float(api_result[to_currency])
                else:
                    # Utlöser ett fel som fångas av except om dictionaryn inte innehåller kursen som behövs.
                    raise ValueError("Exchange rate not found.")

            else:
                # Utlöser ett fel om svaret varken är ett tal eller en dictionary.
                raise ValueError("Unexpected API response.")

        # Multiplicerar beloppet med kursen och sparar det omvandlade beloppet.
        converted_amount = amount_value * rate

    # Visar ett fel med statuskod 502 om kursen saknas eller inte kan användas.
    except (ValueError, TypeError, KeyError):
        return render_template(
            "error.html", fel="Valutakursen kunde inte hämtas. Försök igen."
        ), 502

    # Visar home.html med valutor, belopp, resultat och kurs.
    # show_result=True gör att resultatet visas på sidan.
    return render_template(
        "home.html",
        from_currency=from_currency,
        to_currency=to_currency,
        amount=amount,
        converted_amount=converted_amount,
        exchange_rate=rate,
        show_result=True,
    )


# Kopplar adressen /history till funktionen som visar statistik och diagram.
@app.route("/history")
def history():
    # Läser valutorna från länken till historiksidan.
    # Om valen saknas används SEK som första valuta och EUR som andra.
    from_currency = request.args.get("from", "SEK")
    to_currency = request.args.get("to", "EUR")

    # Om någon valuta saknas i listan visas ett fel med statuskod 400.
    if from_currency not in CURRENCIES or to_currency not in CURRENCIES:
        return render_template("error.html", fel="Välj giltiga valutor"), 400

    # Historiksidan kräver olika valutor, annars visa ett fel med status 400.
    if from_currency == to_currency:
        return render_template(
            "error.html", fel="Välj två olika valutor för historiken."
        ), 400

    # Sätter periodens slutdatum till dagens datum.
    end_date = date.today()
    # Sätter startdatumet till 30 dagar före slutdatumet.
    start_date = end_date - timedelta(days=30)

    # Hämtar valutakurser mellan start och slutdatum och sparas.
    # isoformat() gör om datumen till text som API:t kan läsa.
    historical_data = hämta_tidsserie(
        from_currency,
        to_currency,
        start_date.isoformat(),
        end_date.isoformat(),
    )

    # Om hämtningen misslyckas visas ett felmeddelande med statuskod 502.
    if historical_data is None:
        return render_template(
            "error.html", fel="Historiska kurser kunde inte hämtas. Försök igen."
        ), 502

    # Visar ett felmeddelande om svaret är tomt och saknar kurser.
    if not historical_data:
        return render_template(
            "error.html", fel="Det finns inga valutakurser för perioden."
        ), 502

    try:
        # Gör historiken till en tabell med datum och kurser och sparar den i df.
        df = create_dataframe(historical_data)

        if df.empty:
            raise ValueError("No historical data available.")

        # Gör om datumtexten i kolumnen date till datum som pandas kan jobba med.
        df["date"] = pd.to_datetime(df["date"])
        # Sorterar tabellen från äldsta till senaste datum.
        df = df.sort_values("date")

        # Hämtar högsta och lägsta kursen och sparar i varsin variabel.
        highest_rate, lowest_rate = highest_and_lowest_rate(df)

        # Väljer första kursen i den sorterade tabellen.
        start_rate = df["rate"].iloc[0]
        # Väljer sista kursen i historiken.
        current_rate = df["rate"].iloc[-1]
        # Beräknar förändringen i procent mellan första och sista kursen.
        change = percentage_change(start_rate, current_rate)

        # Skapar ett linjediagram som visar hur valutakursen förändras över tid.
        chart = create_history_chart(df)
        # Räknar ut medelvärdet av valutakurserna för varje månad.
        monthly_data = monthly_average(df)
        # Skapar ett stapeldiagram som visar den genomsnittliga valutakursen för varje månad.
        monthly_chart = create_monthly_average_chart(monthly_data)

    # Fångar felaktiga värden, datatyper, saknade nycklar och division med noll.
    # Visar ett felmeddelande om historiken inte kan bearbetas.
    except (ValueError, TypeError, KeyError, ZeroDivisionError):
        return render_template(
            "error.html", fel="Historiska data kunde inte bearbetas."
        ), 502

    # Visar history.html med diagram och statistik.
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


# Kopllar adressen /about till funktionen som visar informationssidan.
@app.route("/about")
def about():
    return render_template("about.html")


# Visar vår felmall om användaren öppnar en adress som inte finns.
@app.errorhandler(404)
def saknas(e):
    return render_template("error.html", fel="Sidan finns inte"), 404


# Startar servern när filen körs som program.
# debug=True laddar om servern när ändringar sparas och visar felsökning.
if __name__ == "__main__":
    app.run(debug=True)

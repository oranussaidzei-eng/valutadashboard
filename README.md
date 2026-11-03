# valutadashboard

En Flask-app för valutaomvandling som hämtar kurser från Frankfurter API och visar historisk utveckling i diagram.

## Installation

1. Skapa en venv: `py -m venv venv`
2. Aktivera den: `venv/Scripts/activate`
3. Installera paketen: `pip install -r requirements.txt -r requirements-dev.txt`
4. Starta appen: `py -m currency_dashboard.app`

Öppna http://127.0.0.1:5000 i webbläsaren.

## Sidor

- `/` visar valutaformuläret och resultatet av omvandlingen.
- `/history` visar historiska valutakurser, statistik och diagram.
- `/about` visar information om projektet.

## Kontrollera koden

```powershell
ruff check currency_dashboard/app.py tests/test_app.py
ruff format --check currency_dashboard/app.py tests/test_app.py
py -m pytest tests/test_app.py
```

Flask-testerna körs utan nätverk. API-anropen ersätts med mockade svar.

## Paketering

```powershell
pip install build
py -m build
```

Paketfilerna skapas i `dist/`. Python-koden, HTML-mallarna och CSS-filen följer med.

# API-modulen - currency_api.py
Detta är en modul som är en del av Flask-appen som hämtar valutakurser från Frankfurter API och skickar dem vidare, visar även aktuell och historiska kurser.   


## Funktioner

1. `hämta_valutakurs(från_valuta, till_valuta, datum=None)`
    Hämtar kursen mellan två valutor, utan datum hämtas dagens kurs. Med datum hämtas kursen för det datumet. Returnerar kursen som ett decimaltal t.ex. 11.05 eller `None` vid fel.

2. `hämta_tidsserie(från_valuta, till_valuta, startdatum, slutdatum)` 
    Funktionen hämtar valutakursen mellan två valutor för varje dag, mellan startdatum och slutdatum. Funktionen returnerar en lista med dictionaries med kursens tidsserie, en per dag med datum och kurs eller `None` vid fel.


## Kontrollera koden
```
ruff check currency_api.py tests/test_currency_api.py
ruff format --check currency_api.py tests/test_currency_api.py
py -m pytest tests/test_currency_api.py 
```
I testerna ersätts `requests.get` med en mock så att testerna körs utan nätverk och att vi kan testa felfall.

# Nejma – Dataanalys och datavisualisering

## Dataanalys – analysis.py

Den här modulen använder Pandas för att bearbeta och analysera historiska valutakurser som hämtas från Frankfurter API.

### Funktioner

1. `create_dataframe(historical_data)` – Omvandlar historiska valutakurser till en Pandas DataFrame med kolumnerna `date` och `rate`. Funktionen kan hantera data i form av en lista eller en dictionary.

2. `percentage_change(start_rate, end_rate)` – Beräknar den procentuella förändringen mellan två valutakurser. Resultatet avrundas till två decimaler.

3. `monthly_average(df)` – Omvandlar datum till rätt datumformat, grupperar valutakurserna per månad med `groupby()` och beräknar medelvärdet för varje månad.

4. `highest_and_lowest_rate(df)` – Tar fram den högsta och lägsta valutakursen under den valda perioden.

## Datavisualisering – charts.py

Den här modulen använder Plotly för att skapa diagram som visualiserar historiska valutakurser och resultat från dataanalysen.

### Funktioner

1. `style_chart(fig)` – Anpassar diagrammens utseende med gemensamma färger, typsnitt, bakgrund och axelinställningar.

2. `create_history_chart(df)` – Skapar ett linjediagram som visar hur valutakursen förändras över tid.

3. `create_monthly_average_chart(monthly_data)` – Skapar ett stapeldiagram som visar den genomsnittliga valutakursen per månad.

Diagrammen omvandlas till HTML med `fig.to_html()` och visas på History-sidan i Flask-applikationen.

## Kontrollera koden

Vi använder Ruff för att kontrollera kodstil och formatering samt Pytest för att testa funktionerna.

Kontrollera kodstilen:

```bash
ruff check currency_dashboard/analysis.py currency_dashboard/charts.py tests/test_analysis.py tests/test_charts.py
```

Kontrollera formateringen:

```bash
ruff format --check currency_dashboard/analysis.py currency_dashboard/charts.py tests/test_analysis.py tests/test_charts.py
```

Kör testerna:

```bash
python -m pytest tests/test_analysis.py tests/test_charts.py -v
```

## Tester

Testerna finns i två filer:

- `tests/test_analysis.py` – Innehåller fem tester som kontrollerar att dataanalysen ger förväntade resultat, bland annat procentuell förändring, månadsmedelvärde samt högsta och lägsta valutakurs.
- `tests/test_charts.py` – Innehåller två tester som kontrollerar att Plotly skapar HTML med rätt axeltexter och diagramfärg.

Totalt innehåller dessa två testfiler sju tester. Testerna använder exempeldata och behöver inga API-anrop
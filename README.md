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

Totalt innehåller dessa två testfiler sju tester. Testerna använder exempeldata och behöver inga API-anrop.

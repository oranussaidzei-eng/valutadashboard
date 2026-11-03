# Dataanalys – Pandas

Vi använder Pandas för att bearbeta och analysera historiska valutakurser som hämtas från Frankfurter API.

Dataanalysen finns i `currency_dashboard/analysis.py` och innehåller fyra funktioner:

- `create_dataframe()` – Omvandlar historiska valutakurser till en DataFrame med datum och valutakurs.
- `percentage_change()` – Beräknar den procentuella förändringen mellan två valutakurser.
- `monthly_average()` – Grupperar valutakurser per månad med `groupby()` och beräknar månadsmedelvärdet.
- `highest_and_lowest_rate()` – Tar fram den högsta och lägsta valutakursen under perioden.

## Datavisualisering – Plotly

Vi använder Plotly för att visualisera resultaten från dataanalysen.

Diagrammen skapas i `currency_dashboard/charts.py`:

- **Linjediagram:** Visar valutakursens historiska utveckling.
- **Stapeldiagram:** Visar den genomsnittliga valutakursen per månad.

Funktionen `style_chart()` används för att ge diagrammen en gemensam design.

Diagrammen omvandlas till HTML med `fig.to_html()` och visas på History-sidan i Flask-applikationen.

## Testning – Pandas och Plotly

Vi använder Pytest för att kontrollera att funktionerna ger förväntade resultat.

- `tests/test_analysis.py` innehåller fem tester för dataanalysen.
- `tests/test_charts.py` innehåller två tester för diagrammen.

Testerna kontrollerar bland annat procentuell förändring, månadsmedelvärden, högsta och lägsta valutakurs samt att Plotly skapar HTML med rätt axeltexter.

För att köra testerna:

```bash
python -m pytest tests/test_analysis.py tests/test_charts.py -v
```

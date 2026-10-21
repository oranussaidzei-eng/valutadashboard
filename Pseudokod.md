Currency Dashboard
Valutor: SEK – USD – EUR – TND – AFN – CDF

Appen ska kunna:
1. Välja från-valuta, t.ex. SEK.
2. Välja till-valuta, t.ex. TND.
3. Skriva in ett belopp, t.ex. 1000.
4. Hämta den senaste tillgängliga valutakursen från Frankfurter API.
5. Beräkna och visa resultatet, t.ex. 1000 SEK = 305 TND.
6. Hämta historiska valutakurser och visa utvecklingen i en graf.
7. Presentera informationen tydligt i en Flask-dashboard.




               CURRENCY DASHBOARD
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
    Kevin         Nejma          Oranus

        API            PANDAS          FLASK
         │               │               │
 currency_api.py     analysis.py       app.py
         │               │               │
      JSON          beräkningar       Jinja
                         │               │
                      groupby          Plotly
          └──────────────┼──────────────┘
                         ↓
                  KOPPLA IHOP ALLT




                  

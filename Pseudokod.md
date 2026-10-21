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
        Kevin          Nejma          Oranus

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


valutadashboard/                  ← repots rotmapp
├── currency_dashboard/           ← själva programmet (Python-paketet)
│   ├── __init__.py               (tom fil)
│   ├── config.py                 konstanter: valutor, adress, timeout
│   ├── currency_api.py           hämtar data från Frankfurter (Kevin)
│   ├── analysis.py               Pandas-beräkningar (Nejma)
│   ├── charts.py                 Plotly-diagram (Nejma)
│   ├── app.py                    Flask: routes (Oranus)
│   └── templates/                (Oranus)
│       ├── base.html
│       ├── index.html
│       ├── history.html
│       ├── monthly.html
│       └── error.html
├── tests/
│   ├── test_currency_api.py      (Kevin)
│   ├── test_analysis.py          (Nejma)
│   ├── test_charts.py            (Nejma)
│   └── test_app.py               (Oranus)
├── docs/
│   └── Pseudokod.md              flytta hit er pseudokod
├── .gitignore
├── README.md
├── requirements.txt
├── requirements-dev.txt
└── pyproject.toml                (läggs till vid paketeringen, lektion 8)

                  

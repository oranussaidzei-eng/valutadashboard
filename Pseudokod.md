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


Currency Dashboard – Pseudokod

Valutor: SEK, USD, EUR, TND, AFN, CDF

Appens funktion:
Användaren väljer en från-valuta och en till-valuta.
Användaren skriver in ett belopp som ska konverteras.
Programmet kontrollerar att beloppet är giltigt.

Om användarens input är korrekt hämtas den senaste tillgängliga
valutakursen från Frankfurter API.

Programmet beräknar det nya beloppet:
konverterat belopp = belopp * valutakurs

Resultatet visas för användaren.
Exempel: 1000 SEK = X TND.

Programmet hämtar även historiska valutakurser från Frankfurter API.
Den historiska datan skickas vidare för analys med Pandas.

Kevin – API (currency_api.py)

Kevin ansvarar för att:
- Hämta senaste tillgängliga valutakurs från Frankfurter API.
- Hämta historiska valutakurser.
- Hantera JSON-data från API:t.
- Använda timeout vid API-anrop.
- Hantera fel om API:t inte fungerar.
- Programmet ska visa ett tydligt felmeddelande istället för att krascha.

Nejma – Pandas och Plotly (analysis.py och charts.py)

Nejma tar emot den historiska datan från currency_api.py.

I analysis.py:
- Skapa en Pandas DataFrame av den historiska datan.
- Bearbeta datum och valutakurser.
- Skapa en ny kolumn med procentuell förändring.
- Använda groupby() för att gruppera data per månad.
- Beräkna genomsnittlig valutakurs per månad.
- Hitta högsta valutakursen under perioden.
- Hitta lägsta valutakursen under perioden.

I charts.py:
- Skapa ett linjediagram med Plotly som visar valutakursens
  utveckling över tid.
- Skapa ett stapeldiagram med Plotly som visar den
  genomsnittliga valutakursen per månad.
- Diagrammen ska ha titel samt namn på X- och Y-axlar.

Oranus – Flask och Jinja (app.py och templates)

Oranus ansvarar för Flask-applikationen.

Startsidan ska låta användaren:
- Välja från-valuta.
- Välja till-valuta.
- Skriva in ett belopp.
- Starta konverteringen.

Flask ska koppla ihop API-delen, Pandas-delen och Plotly-delen.

Routes:
"/" visar startsidan.
"/history" visar valutakonverteringen och historisk utveckling.
"/monthly" visar månadsanalysen.

Templates:
base.html – gemensam grund för sidorna.
index.html – formuläret där användaren väljer valuta och belopp.
history.html – resultat och historiskt diagram.
monthly.html – månadsanalys och diagram.
error.html – visar felmeddelanden.

Tester

Kevin:
test_currency_api.py

Nejma:
test_analysis.py
test_charts.py

Oranus:
test_app.py

API-anrop ska mockas i testerna.
Pandas-funktionerna ska testas.
Flask-routes ska testas.
Projektet ska innehålla minst 5 tester totalt.

Programmets flöde:

Användare
→ Flask
→ Frankfurter API
→ JSON-data
→ Pandas
→ Beräkningar och groupby
→ Plotly-diagram
→ Jinja
→ Currency Dashboard










                  

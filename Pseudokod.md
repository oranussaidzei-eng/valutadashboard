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












PROJEKT: CURRENCY DASHBOARD

VALUTOR:
SEK
USD
EUR
TND
AFN
CDF


========================================
START
========================================

Starta Flask-applikationen

Visa startsidan


========================================
ANVÄNDARENS VAL
========================================

Användaren väljer:

    från-valuta
    till-valuta
    belopp

Exempel:

    från-valuta = SEK
    till-valuta = TND
    belopp = 1000


Kontrollera användarens input

OM belopp saknas
    visa felmeddelande

OM belopp inte är ett giltigt nummer
    visa felmeddelande

OM belopp är mindre än eller lika med 0
    visa felmeddelande

ANNARS
    fortsätt


========================================
API – KEVIN
currency_api.py
========================================

Ta emot:

    från-valuta
    till-valuta

Skicka GET-request till Frankfurter API

Använd timeout


OM API-anropet lyckas

    läs JSON-svaret

    hämta senaste tillgängliga valutakurs

    spara valutakursen

    hämta datum för valutakursen


    beräkna:

    konverterat belopp =
    belopp * valutakurs


    Exempel:

    1000 SEK = X TND


ANNARS

    hantera API-felet

    skicka tydligt felmeddelande

    programmet ska inte krascha


========================================
HISTORISK DATA – KEVIN
currency_api.py
========================================

Hämta historiska valutakurser
från Frankfurter API

Ta emot:

    från-valuta
    till-valuta
    datum / tidsperiod

Skicka GET-request

OM anropet lyckas

    läs JSON-data

    returnera historiska valutakurser

ANNARS

    hantera felet


========================================
PANDAS – NEJMA
analysis.py
========================================

Ta emot historiska valutakurser
från currency_api.py


Skapa en Pandas DataFrame

DataFrame innehåller exempelvis:

    date
    rate


Sortera datan efter datum


========================================
PROCENTUELL FÖRÄNDRING – NEJMA
analysis.py
========================================

Skapa en ny beräknad kolumn:

    percentage_change


Beräkna hur mycket kursen
förändras procentuellt


========================================
MÅNADSANALYS – NEJMA
analysis.py
========================================

Skapa information om månad
från datumkolumnen


Använd Pandas groupby()

Gruppera valutakurser per månad


Beräkna:

    genomsnittlig kurs per månad


Hitta även:

    högsta kurs

    lägsta kurs

    total procentuell förändring
    under perioden


Returnera resultaten


========================================
PLOTLY – NEJMA
charts.py
========================================

Ta emot bearbetad data
från analysis.py


Skapa diagram 1:

    HISTORISK VALUTAKURS

    diagramtyp = linjediagram

    X-axel = datum

    Y-axel = valutakurs


Skapa diagram 2:

    GENOMSNITTLIG KURS PER MÅNAD

    diagramtyp = stapeldiagram

    X-axel = månad

    Y-axel = genomsnittlig valutakurs


Lägg till:

    titel
    namn på X-axel
    namn på Y-axel


Returnera diagrammen


========================================
FLASK – ORANUS
app.py
========================================

Skapa Flask-applikationen


ROUTE:

/

Visa startsidan

Använd:

    index.html


ROUTE:

/history

Ta emot användarens:

    från-valuta
    till-valuta
    belopp


Anropa currency_api.py

Hämta:

    senaste kurs
    historiska kurser


Anropa analysis.py

Hämta:

    analyserad data


Anropa charts.py

Hämta:

    historiskt diagram


Skicka resultatet till:

    history.html


ROUTE:

/monthly

Använd analyserad data

Visa:

    genomsnittlig kurs per månad
    högsta kurs
    lägsta kurs
    procentuell förändring
    månadsdiagram


Använd:

    monthly.html


========================================
JINJA / HTML – ORANUS
========================================

base.html

    gemensam grund för sidorna


index.html

    visa rubrik

    visa från-valuta

    visa till-valuta

    visa belopp

    visa knapp för att söka


history.html

    visa valt valutapar

    visa belopp

    visa senaste valutakurs

    visa konverterat belopp

    visa historisk utveckling

    visa Plotly linjediagram


monthly.html

    visa månadsanalys

    visa genomsnitt per månad

    visa högsta kurs

    visa lägsta kurs

    visa procentuell förändring

    visa Plotly stapeldiagram


error.html

    visa ett tydligt felmeddelande
    om något går fel


========================================
CONFIG
config.py
========================================

Spara gemensamma inställningar:

    valutor:
    SEK
    USD
    EUR
    TND
    AFN
    CDF

    adress till Frankfurter API

    timeout


========================================
TESTER
========================================

KEVIN:

    test_currency_api.py

    testa API-funktionerna

    mocka externa API-anrop


NEJMA:

    test_analysis.py

    testa Pandas-beräkningarna

    testa groupby

    testa procentuell förändring

    testa högsta/lägsta kurs


    test_charts.py

    testa funktionerna som
    skapar diagram


ORANUS:

    test_app.py

    testa Flask-routes

    testa att sidorna svarar korrekt


Minst 5 tester totalt


========================================
HELA PROGRAMMETS FLÖDE
========================================


ANVÄNDARE
     │
     ↓
FLASK – ORANUS
     │
     ↓
currency_api.py – KEVIN
     │
     ↓
FRANKFURTER API
     │
     ↓
JSON
     │
     ↓
analysis.py – NEJMA
     │
     ↓
PANDAS
     │
     ├── procentuell förändring
     ├── groupby per månad
     ├── genomsnitt
     ├── högsta kurs
     └── lägsta kurs
     │
     ↓
charts.py – NEJMA
     │
     ├── linjediagram
     └── stapeldiagram
     │
     ↓
FLASK / JINJA – ORANUS
     │
     ↓
CURRENCY DASHBOARD


========================================
SLUT
========================================

                  

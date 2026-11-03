# valutadashboard

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

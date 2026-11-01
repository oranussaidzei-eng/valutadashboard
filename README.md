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
# patch kan tillfärlligt ersätta API-funktioner
from unittest.mock import patch

# Kör testerna
import pytest

# Importerar webbappen som ska testas.
from currency_dashboard.app import app


# Förbereder en testklient åt varje test som har parametern klient.
@pytest.fixture
def klient():
    # Aktiverar testläge så att fel i appen kan visas i testresultet.
    app.config["TESTING"] = True
    # Skapar en låtsas-webbläsare för att testa appen utan att starta den på riktigt.
    return app.test_client()


# Kontrollera att startsidan öpnnas och innehåller den förvantade texten.
def test_startsida(klient):
    # Öppnar startsidan och sparar svaret i svar.
    svar = klient.get("/")

    # Kontrollerar att förfrågan lyckas och ger statuskod 200.
    assert svar.status_code == 200
    # Läser sidans innehåll som text och kontrollerar att rubriken finns.
    assert "CURRENCY CONVERTER" in svar.get_data(as_text=True)


# Ersätter hämta_valutakurs i app.py så att den ger kursen 0.10.
# Den riktiga API-funktionen körs inte.
@patch("currency_dashboard.app.hämta_valutakurs", return_value=0.10)
def test_giltigt_formular(mock_kurs, klient):
    # Samlar valutorna och beloppet som testet skickar till startsidan.
    formular = {
        "from_currency": "SEK",
        "to_currency": "USD",
        "amount": "25",
    }

    # Skickar testets inmatning till startsidan och sparar Flask svar.
    svar = klient.post("/", data=formular)

    # Kontrollerar att förfrågan lyckas och ger statuskod 200.
    assert svar.status_code == 200
    # Kontrollerar att 25 gånger kursen 0.10 visar som 2.50 USD på sidan.
    assert "2.50 USD" in svar.get_data(as_text=True)


# Testar att appen stoppar ett negativt belopp.
def test_negativt_belopp(klient):
    # Samlar valutorna och beloppet som testet skickar till startsidan.
    formular = {
        "from_currency": "SEK",
        "to_currency": "USD",
        "amount": "-10",
    }

    # Skickar testets inmatning till startsidan och sparar flask svar.
    svar = klient.post("/", data=formular)

    # Kontrollerar att felaktig inmatning avvisas med statuskod 400.
    assert svar.status_code == 400
    # Kontrollerar att felmeddelandet för beloppet visas på sidan.
    assert "Ange ett giltigt belopp större än noll." in svar.get_data(as_text=True)


# Ersätter historikfunktionen så att testet inte behöver internet.
@patch("currency_dashboard.app.hämta_tidsserie")
def test_historiksida(mock_historik, klient):
    # Analys och diagramfunktionerna använder dessa värden under testet.
    mock_historik.return_value = [
        {"date": "2026-09-01", "rate": 0.10},
        {"date": "2026-09-02", "rate": 0.12},
        {"date": "2026-09-03", "rate": 0.11},
    ]

    # Öppnar historiksidan med SEK och USD som valda valutor.
    svar = klient.get("/history?from=SEK&to=USD")

    # Kontrollerar att förfrågan lyckas och ger statuskod 200.
    assert svar.status_code == 200
    # Kontrollerar att rubriken för historikdiagrammet finns i sidan.
    assert "Exchange Rate History" in svar.get_data(as_text=True)
    # Kontrollerar att rubriken för månadsdiagrammet också finns på sidan.
    assert "Monthly Averages" in svar.get_data(as_text=True)


# Ersätter den riktiga hämtningen med ett tomt svar (None) för att kontrollera,
# att appen inte kraschar när extern data saknas.
@patch("currency_dashboard.app.hämta_valutakurs", return_value=None)
def test_api_fel(mock_kurs, klient):
    # Samlar valutorna och beloppet som testet skickar till startsidan.
    formular = {
        "from_currency": "SEK",
        "to_currency": "USD",
        "amount": "25",
    }

    # Skickar testets inmatning till startsidan och sparar Flasks svar.
    svar = klient.post("/", data=formular)

    # Kontrollerar att den misslyckade kurshämtningen ger statuskod 502.
    assert svar.status_code == 502
    # Kontrollerar att sidan förklarar att valutakursen inte kunde hämtas.
    assert "Valutakursen kunde inte hämtas." in svar.get_data(as_text=True)


# Kontrollerar att en okänd adress visar statuskoden 404.
def test_saknad_sida(klient):
    # Försöker öppna en adress som inte finns i appen routes.
    svar = klient.get("/finns-inte")

    # Kontrollerar att en adress som saknas ger statuskod 404.
    assert svar.status_code == 404
    # Kontrollerar att texten "Sidan finns inte" faktiskt syns på skärmen i webbläsaren.
    assert "Sidan finns inte" in svar.get_data(as_text=True)

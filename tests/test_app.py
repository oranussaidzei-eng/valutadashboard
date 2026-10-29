from unittest.mock import patch

import pytest

from currency_dashboard.app import app


@pytest.fixture
def klient():
    app.config["TESTING"] = True
    return app.test_client()


def test_startsida(klient):
    svar = klient.get("/")

    assert svar.status_code == 200
    assert "CURRENCY CONVERTER" in svar.get_data(as_text=True)


@patch("currency_dashboard.app.hämta_valutakurs", return_value=0.10)
def test_giltigt_formular(mock_kurs, klient):
    formular = {
        "from_currency": "SEK",
        "to_currency": "USD",
        "amount": "25",
    }

    svar = klient.post("/", data=formular)

    assert svar.status_code == 200
    assert "2.50 USD" in svar.get_data(as_text=True)


def test_negativt_belopp(klient):
    formular = {
        "from_currency": "SEK",
        "to_currency": "USD",
        "amount": "-10",
    }

    svar = klient.post("/", data=formular)

    assert svar.status_code == 400
    assert "Ange ett giltigt belopp större än noll." in svar.get_data(as_text=True)


@patch("currency_dashboard.app.hämta_tidsserie")
def test_historiksida(mock_historik, klient):
    mock_historik.return_value = [
        {"date": "2026-09-01", "rate": 0.10},
        {"date": "2026-09-02", "rate": 0.12},
        {"date": "2026-09-03", "rate": 0.11},
    ]

    svar = klient.get("/history?from=SEK&to=USD")

    assert svar.status_code == 200
    assert "Exchange Rate History" in svar.get_data(as_text=True)
    assert "Monthly Averages" in svar.get_data(as_text=True)


@patch("currency_dashboard.app.hämta_valutakurs", return_value=None)
def test_api_fel(mock_kurs, klient):
    formular = {
        "from_currency": "SEK",
        "to_currency": "USD",
        "amount": "25",
    }

    svar = klient.post("/", data=formular)

    assert svar.status_code == 502
    assert "Valutakursen kunde inte hämtas." in svar.get_data(as_text=True)


def test_saknad_sida(klient):
    svar = klient.get("/finns-inte")

    assert svar.status_code == 404
    assert "Sidan finns inte" in svar.get_data(as_text=True)

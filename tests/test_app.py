import pytest

from currency_dashboard.app import app


@pytest.fixture
def klient():
    app.config["TESTING"] = True
    return app.test_client()


def test_startsida(klient):
    svar = klient.get("/")
    assert svar.status_code == 200
    assert "Valutaomvandlare" in svar.get_data(as_text=True)


def test_saknad_sida(klient):
    svar = klient.get("/finns-inte")
    assert svar.status_code == 404
    assert "Sidan finns inte" in svar.get_data(as_text=True)


def test_giltigt_formular(klient):
    formular = {
        "fran_valuta": "SEK",
        "till_valuta": "AFN",
        "belopp": "25",
    }

    svar = klient.post("/history", data=formular)

    assert svar.status_code == 200
    assert "Angivet belopp: 25.0 SEK" in svar.get_data(as_text=True)


def test_negativt_belopp(klient):
    formular = {
        "fran_valuta": "SEK",
        "till_valuta": "AFN",
        "belopp": "-10",
    }

    svar = klient.post("/history", data=formular)

    assert svar.status_code == 400
    assert "Beloppet måste vara större än noll." in svar.get_data(as_text=True)


def test_ogiltig_valuta(klient):
    formular = {
        "fran_valuta": "ABC",
        "till_valuta": "SEK",
        "belopp": "25",
    }

    svar = klient.post("/history", data=formular)

    assert svar.status_code == 400
    assert "Välj giltiga valutor" in svar.get_data(as_text=True)

from unittest.mock import patch

import requests

import currency_api as ca  # Här importerar vi currency_api-modulen från currency_dashboard-paketet och döper den till ca


def test_hämta_valutakurs():  # Här testar vi funktionen
    with patch("currency_api.requests.get") as mock:
        mock.return_value.json.return_value = {"rate": 0.10}

        resultat = ca.hämta_valutakurs("SEK", "USD")

        använd_url = mock.call_args[0][
            0
        ]  # Hämtar den URL som användes vid anropet till requests.get
        använd_timeout = mock.call_args.kwargs[
            "timeout"
        ]  # Hämtar timeout-värdet som användes vid anropet till requests.get

        assert resultat == 0.10
        assert använd_url == "https://api.frankfurter.dev/v2/rate/SEK/USD"
        assert använd_timeout == 5


def test_hämta_historisk_valutakurs():  # Här testar vi funktionen för historisk valutakurs
    with patch(
        "currency_api.requests.get"
    ) as mock:  # Här bestämmer vi att svar.json() ska ge rate 11.1163
        mock.return_value.json.return_value = {"rate": 11.1163}

        resultat = ca.hämta_valutakurs(
            "EUR", "SEK", "2026-09-01"
        )  # Här anropar vi funktionen med specifika valutakoder och datum

        använd_url = mock.call_args[0][0]

        assert (
            resultat == 11.1163
        )  # Funktionen ska returnera den historiska valutakursen som vi mockat
        assert (
            använd_url == "https://api.frankfurter.dev/v2/rate/EUR/SEK?date=2026-09-01"
        )


def test_valutakurs_timeout():
    with patch("currency_api.requests.get") as mock:
        mock.side_effect = requests.exceptions.Timeout

        resultat = ca.hämta_valutakurs("SEK", "USD")

        assert resultat is None  # Funktionen ska returnera None vid timeout


def test_valutakurs_saknar_rate():
    with patch("currency_api.requests.get") as mock:
        mock.return_value.json.return_value = {"date": "2026-10-28"}

        resultat = ca.hämta_valutakurs("EUR", "SEK")

        assert resultat is None  # Funktionen ska returnera None om rate saknas i svaret


def test_hämta_tidsserie():
    låtsats_svar = [
        {"date": "2026-09-01", "base": "SEK", "quote": "TND", "rate": 0.30436},
        {"date": "2026-09-02", "base": "SEK", "quote": "TND", "rate": 0.30328},
    ]

    with patch("currency_api.requests.get") as mock:
        mock.return_value.json.return_value = låtsats_svar

        resultat = ca.hämta_tidsserie("SEK", "TND", "2026-09-01", "2026-09-02")

        använd_url = mock.call_args[0][
            0
        ]  # Hämtar den URL som användes vid anropet till requests.get

        assert resultat == låtsats_svar
        assert len(resultat) == 2
        assert använd_url == (
            "https://api.frankfurter.dev/v2/rates"
            "?base=SEK&quotes=TND&from=2026-09-01&to=2026-09-02"
        )


def test_tidsserie_api_fel():
    with patch("currency_api.requests.get") as mock:
        mock.side_effect = requests.exceptions.ConnectionError

        resultat = ca.hämta_tidsserie("SEK", "TND", "2026-09-01", "2026-09-02")

        assert resultat is None  # Funktionen ska returnera None vid timeout

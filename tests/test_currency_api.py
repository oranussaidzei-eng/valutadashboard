import currency_api as ca # Här importerar vi currency_api-modulen från currency_dashboard-paketet och döper den till ca
from unittest.mock import patch 
def test_hämta_valutakurs(): # Här testar vi funktionen
    resultat = ca.hämta_valutakurs("SEK", "USD") # koden hämtar valutakursen mellan SEK och USD
    assert resultat is not None # koden kontrollerar att valutakursen inte är None

def test_hämta_historisk_valutakurs(): # Här testar vi funktionen för historisk valutakurs
    historiskt_resultat = ca.hämta_historisk_valutakurs("EUR", "SEK", "2026-09-01") # koden hämtar den historiska valutakursen mellan EUR och SEK för det specifika datumet
    assert historiskt_resultat is not None # koden kontrollerar att den historiska valutakursen inte är None

def test_valutakurs_med_mock(): # Här skapar vi den tredje testfunktionen som använder en mock för att testa valutakursfunktionen utan att göra riktiga API-anrop.
    with patch("currency_api.requests.get") as mock: # Vid den här koden så ersätter vi tillfälligt requests.get med en mock-objekt
        mock.return_value.json.return_value = {"rate": 0.10} # Här anger vi vad mock-objektet ska returnera när json() anropas
        resultat = ca.hämta_valutakurs("SEK", "USD") # Vid den här koden så anropar vi funktionen 
        assert resultat == 0.10 # Här kontrollerar vi att resultatet är det vi mockade
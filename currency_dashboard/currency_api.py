import requests  # Importerar requests-biblioteket för att göra HTTP-förfrågningar

BAS_URL = "https://api.frankfurter.dev/v2"  # Bas-URL för Frankfurter API:et
TIMEOUT = 5  # Timeout för API-förfrågningar i sekunder


def hämta_valutakurs(
    från_valuta, till_valuta, datum=None
):  # Hämtar vi valutakursen mellan två valutor
    if datum:  # Om ett datum anges, inkludera det i URL:en
        url = f"{BAS_URL}/rate/{från_valuta}/{till_valuta}?date={datum}"  # Skapar URL:en för API-förfrågan med datum
    else:  # Om inget datum anges, använd standard-URL:en utan datumparameter
        url = f"{BAS_URL}/rate/{från_valuta}/{till_valuta}"  # Skapar URL:en för API-förfrågan

    try:
        svar = requests.get(
            url, timeout=TIMEOUT
        )  # Skapar variabelns svar som skickar GET-förfrågan till API:et och väntar högst 5 sekunder
        svar.raise_for_status()  # Kontrollerar om API-förfrågan lyckades, annars kastas ett undantag
        data = svar.json()  # Omvandlar API-svaret till JSON-format
        valutakurs = data[
            "rate"
        ]  # Hämtar värdet som tillhör nyckeln "rate" i JSON-datan
        return valutakurs  # Returnerar den hämtade valutakursen
    except (
        requests.exceptions.RequestException
    ) as e:  # Hanterar eventuella fel vid API-förfrågan
        print(
            f"Fel vid hämtning av valutakurs: {e}"
        )  # Skriver ut felmeddelandet om API-förfrågan misslyckas
        return None  # Returnerar None om ett fel uppstår vid API-förfrågan
    except KeyError as e:  # Hanterar om "rate" inte finns i JSON-datan
        print(
            f"API-svaret saknar en förväntad nyckel {e}"
        )  # Skriver ut felmeddelandet om "rate" saknas
        return None  # Returnerar None om ett fel uppstår vid hämtning av valutakursen


def hämta_tidsserie(
    från_valuta, till_valuta, startdatum, slutdatum
):  # Hämtar tidsserie för valutakurs mellan två valutor
    url = f"{BAS_URL}/rates?base={från_valuta}&quotes={till_valuta}&from={startdatum}&to={slutdatum}"  # Skapar URL:en för API-förfrågan med start- och slutdatum
    try:
        svar = requests.get(
            url, timeout=TIMEOUT
        )  # Skapar variabelns svar som skickar GET-förfrågan till API:et och väntar högst 5 sekunder
        svar.raise_for_status()  # Kontrollerar om API-förfrågan lyckades, annars kastas ett undantag
        return svar.json()
    except (
        requests.exceptions.RequestException
    ) as e:  # Hanterar eventuella fel vid API-förfrågan
        print(
            f"Fel vid hämtning av tidsserie: {e}"
        )  # Skriver ut felmeddelandet om API-förfrågan misslyckas
        return None  # Returnerar None om ett fel uppstår vid API-förfrågan


if __name__ == "__main__":  # Körs endast om filen körs direkt, inte vid import
    resultat = hämta_valutakurs("SEK", "USD")
    print(resultat)  # Skriver ut den hämtade valutakursen

    historiskt_resultat = hämta_valutakurs("EUR", "SEK", "2026-09-01")
    print(historiskt_resultat)  # Skriver ut den hämtade historiska valutakursen

    tidsserie = hämta_tidsserie("EUR", "SEK", "2026-09-01", "2026-09-05")
    print(tidsserie)  # Skriver ut den hämtade tidsserien

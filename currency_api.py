import requests # Importerar requests-biblioteket för att göra HTTP-förfrågningar

def hämta_valutakurs(från_valuta, till_valuta): # Hämtar vi valutakursen mellan två valutor
    url = f"https://api.frankfurter.dev/v2/rate/{från_valuta}/{till_valuta}" # Skapar URL:en för API-förfrågan
    try:
        svar = requests.get(url, timeout=5) # Skapar variabelns svar som skickar GET-förfrågan till API:et och väntar högst 5 sekunder
        svar.raise_for_status() # Kontrollerar om API-förfrågan lyckades, annars kastas ett undantag
        data = svar.json() # Omvandlar API-svaret till JSON-format 
        valutakurs = data["rate"] # Hämtar värdet som tillhör nyckeln "rate" i JSON-datan
        return valutakurs # Returnerar den hämtade valutakursen
    except requests.exceptions.RequestException as e: # Hanterar eventuella fel vid API-förfrågan
        print(f"Fel vid hämtning av valutakurs: {e}") # Skriver ut felmeddelandet om API-förfrågan misslyckas
        return None # Returnerar None om ett fel uppstår vid API-förfrågan
    except KeyError as e: # Hanterar om "rate" inte finns i JSON-datan
        print(f"API-svaret saknar en förväntad nyckel {e}") # Skriver ut felmeddelandet om "rate" saknas
        return None # Returnerar None om ett fel uppstår vid hämtning av valutakursen

resultat = hämta_valutakurs("SEK", "USD") # Här anropar vi funktionen för att hämta valutakursen mellan SEK och USD
print(resultat) # Skriver ut den hämtade valutakursen

def hämta_historisk_valutakurs(från_valuta, till_valuta, datum): # Hämtar historisk valutakurs för ett specifikt datum
    
    url = f"https://api.frankfurter.dev/v2/rate/{från_valuta}/{till_valuta}?date={datum}" # Skapar URL:en för API-förfrågan med datum
    try:
        svar = requests.get(url, timeout=5) # Skapar variabelns svar som skickar GET-förfrågan till API:et och väntar högst 5 sekunder
        svar.raise_for_status() # Kontrollerar om API-förfrågan lyckades, annars kastas ett undantag
        data = svar.json() # Omvandlar API-svaret till JSON-format 
        valutakurs = data["rate"] # Hämtar värdet som tillhör nyckeln "rate" i JSON-datan
        return valutakurs # Returnerar den hämtade valutakursen
    except requests.exceptions.RequestException as e: # Hanterar eventuella fel vid API-förfrågan
        print(f"Fel vid hämtning av historisk valutakurs: {e}") # Skriver ut felmeddelandet om API-förfrågan misslyckas
        return None # Returnerar None om ett fel uppstår vid API-förfrågan
    except KeyError as e: # Hanterar om "rate" inte finns i JSON-datan
        print(f"API-svaret saknar en förväntad nyckel {e}") # Skriver ut felmeddelandet om "rate" saknas
        return None # Returnerar None om ett fel uppstår vid hämtning av valutakursen

historiskt_resultat = hämta_historisk_valutakurs("EUR", "SEK", "2026-09-01")
print(historiskt_resultat) # Skriver ut den hämtade historiska valutakursen



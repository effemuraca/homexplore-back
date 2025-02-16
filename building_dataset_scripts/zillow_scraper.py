import re
import json
import time
import requests
import pandas as pd
import random


def get_page_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(f"Pagina recuperata: {url}")
        return response.text
    else:
        print(f"Errore {response.status_code} nel recupero della pagina: {url}")
        return None


# Funzione principale per eseguire lo scraping
def scrape_zillow(city:str, state:str, n_pages:int=5):
    base_url = f"https://www.zillow.com/{city}-{state}/"
    all_properties = []

    for page in range(1, n_pages):  #IL RANGE DEFINISCE IL NUMERO DI PAGINE DA SCRAPARE
        url = f"{base_url}{page}_p/"
        print(f"Recupero della pagina: {url}")
        html_content = get_page_content(url)
        print(len(html_content))
        
        html_content = html_content[-300000:]
        pattern = r'"cat1":(\{.*?"searchResults":\{.*?"listResults":\[\{.*?\}\]\}\})'

        # Cerca il pattern nel contenuto HTML
        match = re.search(pattern, html_content, re.DOTALL)

        cat1_search_results_data = None
        if match:
            cat1_search_results_json = match.group(1)
            indice = cat1_search_results_json.find(',"mapResults"')
            # Taglia la stringa se la sottostringa è stata trovata
            if indice != -1:
                cat1_search_results_json = cat1_search_results_json[:indice]
            print(cat1_search_results_json[:1000])
            print(len(cat1_search_results_json))
            # Prendi l'array JSON con i risultati della ricerca
            cat1_search_results_json = cat1_search_results_json.split('"listResults":')[1]
            
            # Converti la stringa JSON in un oggetto Python
            try:
                cat1_search_results_data = json.loads(cat1_search_results_json)
                print("Dati estratti con successo:", cat1_search_results_data)
            except json.JSONDecodeError as e:
                print(e)
                print("Errore nella decodifica del JSON.")
        else:
            print("Non è stato possibile trovare 'cat1' con 'searchResults' nel contenuto HTML.")
        
        if cat1_search_results_data:
            print(cat1_search_results_data)
            all_properties.extend(cat1_search_results_data)
            
        # Tempo random tra 2 e 7 secondi
        time_random = random.randint(2, 7)
        time.sleep(time_random)  # Pausa per evitare di sovraccaricare il server

    # Salva i dati in un file CSV
    file_name = f"properties_{city.lower()}_{state.lower()}.csv"
    df = pd.DataFrame(all_properties)
    df.to_csv(file_name, index=False)
    print(f"Dati salvati in '{file_name}'")
    return all_properties
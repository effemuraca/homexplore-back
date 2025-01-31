# API da implementare nelle routes a partire dai mockup

## map.html

## main.html

- Mostra un numero generico di proprietà casuali nel db (necessaria thumbnail, posizione, prezzo) -> DA FARE OGGI FERDI

## login.html

- Un utente tenta il login

## add_property.html

- Una proprietà viene aggiunta (attenzione al caso end_time < start_time dell'open house) --> FATTO DA ALE E CONSISTENTE SU MONGO

## buyer_reservations.html

- L'utente cancella una prenotazione (tasto cancel) -> FATTO DA FERDI

## edit_profile.html

- Una proprietà viene modificata --> FATTO DA ALE CONSISTENTE SU MONGO

## favourites.html

- Una proprietà viene rimossa dai preferiti -> DA FARE OGGI FERDI

## detail_home.html

- Add to favourites premuto da un buyer -> DA FARE OGGI FERDI
- Book now cliccato da un buyer -> DA FARE OGGI FERDI
- LEVARE INFO SULLE AGENZIE (SIA NEI MOCKUP CHE NELLA COLLECTION PROPERTYONSALE)  --> FATTO SULLE COLLECTION


## seller_dashboard.html
- Edit seller information --> PARZIALMENTE FATTO DA ALE
- View sold houses  --> PARZIALMENTE FATTOI DA ALE
- view property on sale --> PARZIALMENTE FATTO DA ALE

## seller_sold.html

- Cliccato il tasto per cambiare pagina o per andare alla pagina N (andare alla pagina N non ha senso se non si può ordinare per prezzo, etc)
- Predisporre le analytics sulle case vendute (scritte giu)
- Far vedere tutte le case vendute in ordine di prezzo

## seller_for_sale.html

- Il bottone edit property ti porta al form corrispondente alla proprietà (serve l'id della proprietà per propagare la modifica dopo) -> DA FARE OGGI FERDI
- INSERIRE BOTTONE PER ANALYTICS SULLE CASE IN VENDITA
- View Reservations cliccato: mostrate le reservations di una determinata proprietà (info di contatto) -> DA FARE OGGI FERDI
- Sell house --> FATTO DA ALE CONSISTENTE DU MONGO  
- Remove house --> PARZIALMENTE FATTO DA ALE
- INSERIRE BOTTONE PER LA VENDITA(mockup)
- INSERIRE BARRA DI RICERCA(mockup)
- Search an house--> FATTO DA ALE PARZIALEMENTE

## register.html

- Un utente prova a registrarsi 

## superuser_buyers.html, superuser_agencies.html

- La struttura non mi piace, a mio avviso è raro il superuser scorra le agenzie o gli utenti, per cui è fondamentale inserire un filtro di ricerca (sull'id), questo solleva un problema -> le agenzie devono poter vedere gli id degli utenti per poterli segnalare al superuser (che cosi può cancellarli), mentre invece si può supporre che i buyer segnalino le agenzie dopo gli openhouseevent (cosi rimaniamo coerenti alla scelta di non indicare nella pagina di visualizzazione info sull'agenzia)
- Rimozione utente
- Rimozione agenzia
- Gestire il paging (se si vuole tenere la lista con le pagine)

## superuser.html

- Deve presentare (ora non c'è) una card per l'analytic che abbiamo immplementato (ottenere la lista delle agenzie ordinata per introiti /numero di case vendute in un determinato periodo temporale)

## superuser_agencies.html

- View details di un'agenzia (inserire il paging)
- Cliccato il bottone for sale/sold: filtraggio per le case vendute da un'agenzia (con possibilità di cancellare la casa venduta)
- View details cliccato sulla casa in vendita: get sull'id della casa cliccata
- Remove della casa in vendita (usando il bottone Remove)
- INSERIRE NELLA PAGINA DEL SUPERUSER IN CUI VENGONO VISUALIZZATE LE CASE VENDUTE DI UNA SINGOLA AGENZIA BOTTONI PER USARE LE ANALYTICS:
    Data un’agenzia ed una citta ritornare il numero di case vendute e valore ricavato in un determinato periodo temporale  per quartiere;
    Data un’agenzia ed una citta ritornare il tempo medio di vendita di una casa per quartiere
    Data una città elencare gli aumenti dei prezzi al metro quadro per quartiere negli ultimi k mesi    [ordinare per aumento di prezzo crescente]
- INSERIRE NELLA PAGINA DEL SUPERUSER IN CUI VENGONO VISUALIZZATE LE CASE IN VENDITA DI UNA SINGOLA AGENZIA DUE BOTTONI PER USARE LE ANALYTICS:
    Data una città ritornare la media del prezzo al metro quadro delle case in vendita per ogni quartiere [filtro per tipologia di appartamento, ordinare per prezzo decrescente]

## index.html

- search cliccato: parte la get con i parametri che l'utente ha impostato -> DA FARE OGGI FERDI

# search.html

- PAGINA DA CREARE
- bottone show analytics che mostra le analytics buyer per la città scelta quando l'utente ha fatto la ricerca
- explore the area cliccato: aperta la mappa sulla città scelta dall'utente (magari se ha scelto un quartiere la mappa viene aperta sul quartiere)
- paging da implementare

## Miscellanea

- Arriva l'open house event -> DA FARE OGGI FERDI

RIMUOVERE IL SESSO DAI MOCKUP E DALL'UML (che va riguardato tutto)
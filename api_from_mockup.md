# API da implementare nelle routes a partire dai mockup

## map.html

## main.html

- Mostra un numero generico di proprietà casuali nel db (necessaria thumbnail, posizione, prezzo)

## login.html

- Un utente tenta il login

## add_property.html

- Una proprietà viene aggiunta (attenzione al caso end_time < start_time)

## buyer_reservations.html

- L'utente cancella una prenotazione (tasto cancel)

## edit_profile.html

- Una proprietà viene modificata

## favourites.html

- Una proprietà viene rimossa dai preferiti

## detail_home.html

- Add to favourites premuto da un buyer
- Book now cliccato da un buyer
- LEVARE INFO SULLE AGENZIE (SIA NEI MOCKUP CHE NELLA COLLECTION PROPERTYONSALE)

## seller_sold.html

- Cliccato il tasto per cambiare pagina o per andare alla pagina N (andare alla pagina N non ha senso se non si può ordinare per prezzo, etc)
- Predisporre le analytics sulle case vendute (scritte giu)


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

## seller_for_sale.html

- Il bottone edit property ti porta al form corrispondente alla proprietà (serve l'id della proprietà per propagare la modifica dopo)
- INSERIRE BOTTONE PER ANALYTICS SULLE CASE IN VENDITA
- View Reservations cliccato: mostrate le reservations di una determinata proprietà (info di contatto)
- Rimozione della proprietà

## index.html

- search cliccato: parte la get con i parametri che l'utente ha impostato

# search.html

- PAGINA DA CREARE
- bottone show analytics che mostra le analytics buyer per la città scelta quando l'utente ha fatto la ricerca
- explore the area cliccato: aperta la mappa sulla città scelta dall'utente (magari se ha scelto un quartiere la mappa viene aperta sul quartiere)
- paging da implementare

## Miscellanea

- Viene venduta una casa
- Arriva l'open house event

RIMUOVERE IL SESSO DAI MOCKUP E DALL'UML (che va riguardato tutto)
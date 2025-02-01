# API da implementare nelle routes a partire dai mockup

## map.html

DA VEDERE CARLO

## main.html

- Mostra un numero generico di proprietà casuali nel db (necessaria thumbnail, posizione, prezzo) -> CARLO TOGLI QUESTA ROBA DAI MOCKUP

## login.html

- Un utente tenta il login

## add_property.html

- Una proprietà viene aggiunta (attenzione al caso end_time < start_time dell'open house) --> FATTO DA ALE E CONSISTENTE SU MONGO

## buyer_reservations.html

- L'utente cancella una prenotazione (tasto cancel) -> FATTO DA FERDI

## edit_property.html

- Una proprietà viene modificata --> FATTO DA ALE CONSISTENTE SU MONGO / DA FARE FERDI (REDIS + PREFERITI)

## edit_profile.html

- Un utente (buyer o seller) modifica i propri dati -> DA FARE FERDI (REDIS) / QUALCUN ALTRO DEVE FARE MONGO

## favorites.html

- Una proprietà viene rimossa dai preferiti -> FATTO FERDI

## detail_home.html

- Add to favorites premuto da un buyer -> FATTO FERDI
- Book now cliccato da un buyer -> FATTO DA FERDI
- LEVARE INFO SULLE AGENZIE (SIA NEI MOCKUP CHE NELLA COLLECTION PROPERTYONSALE)  --> FATTO SULLE COLLECTION

## seller_dashboard.html

- Edit seller information --> PARZIALMENTE FATTO DA ALE / DA FARE FERDI (REDIS)
- View sold houses  --> PARZIALMENTE FATTOI DA ALE
- view property on sale --> PARZIALMENTE FATTO DA ALE

## seller_sold.html

- Cliccato il tasto per cambiare pagina o per andare alla pagina N (andare alla pagina N non ha senso se non si può ordinare per prezzo, etc)
- Predisporre le analytics sulle case vendute (scritte giu)
- Far vedere tutte le case vendute in ordine di prezzo -> FATTO DA FERDI

## seller_for_sale.html

- Il bottone edit property ti porta al form corrispondente alla proprietà (serve l'id della proprietà per propagare la modifica dopo)
- INSERIRE BOTTONE PER ANALYTICS SULLE CASE IN VENDITA
- View Reservations cliccato: mostrate le reservations di una determinata proprietà (info di contatto) -> FATTO DA FERDI
- Sell house --> FATTO DA ALE CONSISTENTE DU MONGO / DA FARE FERDI (REDIS + PREFERITI)  
- Remove house --> PARZIALMENTE FATTO DA ALE / DA FARE FERDI (REDIS + PREFERITI)
- INSERIRE BOTTONE PER LA VENDITA(mockup)
- INSERIRE BARRA DI RICERCA(mockup)
- Search an house--> FATTO DA ALE PARZIALEMENTE

## register.html

- Un utente prova a registrarsi

## index.html

- search cliccato: parte la get con i parametri che l'utente ha impostato 

## search.html

- PAGINA DA CREARE
- bottone show analytics che mostra le analytics buyer per la città scelta quando l'utente ha fatto la ricerca
- explore the area cliccato: aperta la mappa sulla città scelta dall'utente (magari se ha scelto un quartiere la mappa viene aperta sul quartiere)
- paging da implementare

## Miscellanea

- Arriva l'open house event -> DA FARE FERDI

RIMUOVERE IL SESSO DAI MOCKUP E DALL'UML (che va riguardato tutto)
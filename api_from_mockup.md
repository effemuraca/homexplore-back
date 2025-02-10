# API da implementare nelle routes a partire dai mockup

## NON LOGGATI

### map.html

- Vedere tutte le case in un'area collegate a quella di partenza: GET /map/get_properties
- Vedere i POI collegati a una casa: GET /map/get_pois
DA VEDERE CARLO

### main.html

- Mostra un numero generico di proprietà casuali nel db (necessaria thumbnail, posizione, prezzo) -> FATTO DA FERDI

### register.html

- Un buyer prova a registrarsi: POST /auth/signup/buyer
- Un seller prova a registrarsi: POST /auth/signup/seller

### login.html

- Un buyer o un seller tenta il login: POST /auth/login

- Un buyer o un seller fa il refresh del token: POST /auth/jwt/refresh

### index.html

- search cliccato: parte la get con i parametri che l'utente ha impostato -> FATTO DA FERDI
- CARLO AGGIUNGI COME FILTRO DI RICERCA IL TIPO DI CASA(mockup)

### search.html

- PAGINA DA CREARE: /TO/BE/DECIDED
- explore the area cliccato: aperta la mappa sulla città scelta dall'utente (magari se ha scelto un quartiere la mappa viene aperta sul quartiere)
- paging da implementare

### detail_home.html

- Ottiene le informazioni di quella casa -> FATTO (NORMALE GET BY ID): GET /TO/BE/DECIDED
- LEVARE INFO SULLE AGENZIE (SIA NEI MOCKUP CHE NELLA COLLECTION PROPERTYONSALE)  --> FATTO SULLE COLLECTION + FATTO SUL MOCKUP

## SELLER

### seller.html

### profile.html

- Get all profile info: -> FATTO DA FERDI GET /seller/get_profile_info

### edit_profile.html

- Un utente (buyer o seller) modifica i propri dati -> FATTO FERDI + FATTO MOCKUP : PUT /seller/

### seller_sold.html

- Far vedere tutte le case vendute in ordine di prezzo -> FATTO DA FERDI occhio alla paginazione: GET /seller/sold_properties
- Cliccato il tasto per cambiare pagina o per andare alla pagina N (andare alla pagina N non ha senso se non si può ordinare per prezzo, etc)
- Predisporre le analytics sulle case vendute

### seller_for_sale.html

- Il bottone edit property ti porta al form corrispondente alla proprietà (serve l'id della proprietà per propagare la modifica dopo) -> FATTO (?)
- INSERIRE BOTTONE PER ANALYTICS SULLE CASE IN VENDITA
- View Reservations cliccato: mostrate le reservations di una determinata proprietà (info di contatto) -> FATTO DA FERDI: GET /seller/properties_on_sale/reservations -> CARLO AGGIUNGI UN COUNT DI QUANTI PRENOTATI CI SONO NEI MOCKUP(mockup) FATTO
- Sell house --> FATTO DA ALE CONSISTENTE DU MONGO / DA FARE FERDI (REDIS + PREFERITI): POST /seller/sell_properties_on_sale
- Remove house --> PARZIALMENTE FATTO DA ALE / DA FARE FERDI (REDIS + PREFERITI): DELETE /seller/properties_on_sale
- AGGIUNGERE AI MOCKUP (IN OGNI CARD DI OGNI CASA) IL TASTO "VIEW SCHEDULE", CHE SE CLICCATO SCARICA UN PDF CON LA SCHEDULE DEGLI ORARI E INDIRIZZI IN CUI CI SARANNO OPEN HOUSE EVENT QUEL GIORNO

- INSERIRE BOTTONE PER LA VENDITA(mockup) FATTO
- INSERIRE BARRA DI RICERCA(mockup)
- Search an house--> FATTO DA ALE PARZIALMENTE: POST /seller/search_properties_on_sale

### add_property.html

- Una proprietà viene aggiunta (attenzione al caso end_time < start_time dell'open house) --> FATTO DA ALE E CONSISTENTE SU MONGO: POST /seller/properties_on_sale
- AGGIUNGERE NEI MOCKUP LA SCELTA DI MAX_ATTENDEES
- AGGIUNGERE LA SELECT DEL QUARTIERE E CITTA'

### edit_property.html

- Una proprietà viene modificata --> FATTO DA ALE CONSISTENTE SU MONGO / DA FARE FERDI (REDIS + PREFERITI): PUT /seller/properties_on_sale
- AGGIUNGERE NEI MOCKUP LA SCELTA DI MAX_ATTENDEES

## BUYER

### search.html (buyer)

- bottone show analytics che mostra le analytics buyer per la città scelta quando l'utente ha fatto la ricerca: /TO/BE/DECIDED

### detail_home.html (buyer)

- Add to favourites premuto da un buyer -> FATTO FERDI: POST /buyer/favourites
- Book now cliccato da un buyer -> FATTO DA FERDI: POST /buyer/reservations

### profile.html (buyer)

- Get all profile info -> FATTO DA FERDI: GET /buyer/get_profile_info

### edit_profile.html (buyer)

- Un buyer modifica i propri dati -> FATTO FERDI (REDIS) / QUALCUN ALTRO DEVE FARE MONGO: PUT /buyer

### buyer_reservations.html

- Ottiene tutte le prenotazioni dell'utente -> FATTO DA FERDI: GET /buyer/reservations
- L'utente cancella una prenotazione (tasto cancel) -> FATTO DA FERDI: DELETE /buyer/reservations
- AGGIUNGERE NELLA PAGINA LA SCRITTA "GUARDARE ANCHE PROPERTYONSALE PER ESSERE SICURI CHE LE INFO SIANO AGGIORNATE" O SIMILI
- AGGIUNGERE ANCHE L'INFO RELATIVA AL FATTO CHE LE INFO VERRANNO TRASMESSE AL SELLER E DI STARE ATTENTI A NON MODIFICARE EMAIL E TELEFONO INSIEME
- ASSICURARSI CHE CLICCANDO SULLA RESERVATION SI VADA AL SITO DI DEI DETTAGLI DELLA PROPERTYONSALE

### favourites.html

- Ottiene tutti i preferiti dell'utente -> FATTO DA FERDI: GET /buyer/favourites
- Una proprietà viene rimossa dai preferiti -> FATTO FERDI: DELETE /buyer/favourites

### Miscellanea

- Arriva l'open house event -> FATTO DA FERDI

RIMUOVERE IL SESSO DAI MOCKUP E DALL'UML (che va riguardato tutto)

IN GENERALE I NOMI DELLE ROUTE NON SONO DEFINITIVI

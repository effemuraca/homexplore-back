# API da implementare nelle routes a partire dai mockup

## NON LOGGATI

### map.html

- Vedere tutte le case in un'area filtrate per score: GET /map/get_properties
- Vedere i POI collegati a una casa: GET /map/get_pois
DA VEDERE CARLO

### main.html

- Mostra un numero generico di proprietà casuali nel db (necessaria thumbnail, posizione, prezzo) -> CARLO TOGLI QUESTA ROBA DAI MOCKUP

### register.html

- Un utente prova a registrarsi: POST /auth/signup

### login.html

- Un utente tenta il login: POST /auth/login

### index.html

- search cliccato: parte la get con i parametri che l'utente ha impostato -> FATTO DA FERDI
- CARLO AGGIUNGI COME FILTRO DI RICERCA IL TIPO DI CASA

### search.html

- PAGINA DA CREARE: /TO/BE/DECIDED
- explore the area cliccato: aperta la mappa sulla città scelta dall'utente (magari se ha scelto un quartiere la mappa viene aperta sul quartiere)
- paging da implementare

### detail_home.html

- Ottiene le informazioni di quella casa: GET /TO/BE/DECIDED
- LEVARE INFO SULLE AGENZIE (SIA NEI MOCKUP CHE NELLA COLLECTION PROPERTYONSALE)  --> FATTO SULLE COLLECTION

## SELLER

### seller.html

- Edit seller information --> PARZIALMENTE FATTO DA ALE / DA FARE FERDI (REDIS)
- View sold houses  --> PARZIALMENTE FATTOI DA ALE
- View property on sale --> PARZIALMENTE FATTO DA ALE

### profile.html

- Get all profile info: GET /seller/get_profile_info

### edit_profile.html

- Un utente (buyer o seller) modifica i propri dati -> DA FARE FERDI (REDIS) / QUALCUN ALTRO DEVE FARE MONGO : PUT /seller/

### seller_sold.html

- Far vedere tutte le case vendute in ordine di prezzo -> FATTO DA FERDI occhio alla paginazione: GET /seller/sold_properties
- Cliccato il tasto per cambiare pagina o per andare alla pagina N (andare alla pagina N non ha senso se non si può ordinare per prezzo, etc)
- Predisporre le analytics sulle case vendute (scritte giu)

### seller_for_sale.html

- Il bottone edit property ti porta al form corrispondente alla proprietà (serve l'id della proprietà per propagare la modifica dopo)
- INSERIRE BOTTONE PER ANALYTICS SULLE CASE IN VENDITA
- View Reservations cliccato: mostrate le reservations di una determinata proprietà (info di contatto) -> FATTO DA FERDI: GET /seller/property_on_sale
- Sell house --> FATTO DA ALE CONSISTENTE DU MONGO / DA FARE FERDI (REDIS + PREFERITI): POST /seller/sell_property_on_sale
- Remove house --> PARZIALMENTE FATTO DA ALE / DA FARE FERDI (REDIS + PREFERITI): DELETE /seller/property_on_sale

- INSERIRE BOTTONE PER LA VENDITA(mockup)
- INSERIRE BARRA DI RICERCA(mockup)
- Search an house--> FATTO DA ALE PARZIALMENTE: POST /seller/search_property_on_sale

### add_property.html

- Una proprietà viene aggiunta (attenzione al caso end_time < start_time dell'open house) --> FATTO DA ALE E CONSISTENTE SU MONGO: POST /seller/property_on_sale

### edit_property.html

- Una proprietà viene modificata --> FATTO DA ALE CONSISTENTE SU MONGO / DA FARE FERDI (REDIS + PREFERITI): PUT /seller/property_on_sale

## BUYER

### search.html (buyer)

- bottone show analytics che mostra le analytics buyer per la città scelta quando l'utente ha fatto la ricerca: /TO/BE/DECIDED

### detail_home.html (buyer)

- Add to favorites premuto da un buyer -> FATTO FERDI: POST /buyer/favourites
- Book now cliccato da un buyer -> FATTO DA FERDI: POST /buyer/reservations

### profile.html (buyer)

- Get all profile info: GET /buyer/get_profile_info

### edit_profile.html (buyer)

- Un buyer modifica i propri dati -> DA FARE FERDI (REDIS) / QUALCUN ALTRO DEVE FARE MONGO: PUT /buyer

### buyer_reservations.html

- Ottiene tutte le prenotazioni dell'utente: GET /buyer/reservations
- L'utente cancella una prenotazione (tasto cancel) -> FATTO DA FERDI: DELETE /buyer/reservations

### favorites.html

- Ottiene tutti i preferiti dell'utente: GET /buyer/favourites
- Una proprietà viene rimossa dai preferiti -> FATTO FERDI: DELETE /buyer/favourites

### Miscellanea

- Arriva l'open house event -> DA FARE FERDI

RIMUOVERE IL SESSO DAI MOCKUP E DALL'UML (che va riguardato tutto)

IN GENERALE I NOMI DELLE ROUTE NON SONO DEFINITIVI
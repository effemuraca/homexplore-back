# API da implementare nelle routes a partire dai mockup

## NON LOGGATI

### map.html

- Vedere il quartiere e la città di una casa: GET /guest/map/city_and_neighborhood
- Vedere tutte le case in un'area collegate a quella di partenza, compresa sé stessa: GET /guest/map/properties_near_property
- Vedere i POI collegati a una casa: GET /guest/map/pois_near_property

### main.html

- Mostra un numero generico di proprietà casuali nel db: GET /guest/properties_on_sale/random_properties

### register.html

- Un buyer prova a registrarsi: POST /auth/signup/buyer
- Un seller prova a registrarsi: POST /auth/signup/seller

### login.html

- Un buyer o un seller tenta il login: POST /auth/login
- Un buyer o un seller fa il refresh del token: POST /auth/jwt/refresh

### index.html

- search cliccato: parte la get con i parametri che l'utente ha impostato: GET /guest/properties_on_sale/search

### detail_home.html

- Ottiene le informazioni di quella casa: GET /guest/property_on_sale/{property_on_sale_id}

## SELLER

### seller.html

### profile.html

- Get all profile info: GET /seller/get_profile_info

### edit_profile.html

- Un utente (buyer o seller) modifica i propri dati: PUT /seller/

### seller_sold.html

- Far vedere tutte le case vendute in ordine di prezzo: GET /seller/sold_properties

### seller_for_sale.html

- View Reservations cliccato: mostrate le reservations di una determinata proprietà (info di contatto): GET /seller/property_on_sale/reservations
- Sell property: POST /seller/sell_property_on_sale
- Remove property DELETE /seller/property_on_sale

- Get the seller properties: GET /seller/properties_on_sale

### add_property.html

- Una proprietà viene aggiunta (attenzione al caso end_time < start_time dell'open house): POST /seller/property_on_sale

### edit_property.html

- Una proprietà viene modificata: PUT /seller/property_on_sale

## BUYER

### index.html (buyer)

- POST /registered-user/analytics_1
- POST /registered-user/analytics_4
- POST /registered-user/analytics_5

### detail_home.html (buyer)

- Add to favourites premuto da un buyer: POST /buyer/favourites
- Book now cliccato da un buyer: POST /buyer/reservations

### profile.html (buyer)

- Get all profile info: GET /buyer/get_profile_info

### edit_profile.html (buyer)

- Un buyer modifica i propri dati: PUT /buyer

### buyer_reservations.html

- Ottiene tutte le prenotazioni dell'utente: GET /buyer/reservations
- L'utente cancella una prenotazione (tasto cancel): DELETE /buyer/reservations

### favourites.html

- Ottiene tutti i preferiti dell'utente: GET /buyer/favourites
- Una proprietà viene rimossa dai preferiti: DELETE /buyer/favourites

### Miscellanea

RIMUOVERE IL SESSO DAI MOCKUP E DALL'UML (che va riguardato tutto)
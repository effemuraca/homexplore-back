# API full list


## AUTH

- POST /auth/signup/buyer
- POST /auth/signup/seller

- POST /auth/login
- POST /auth/jwt/refresh


## GUEST(non loggati)

- GET /guest/map/properties_near_property
- GET /guest/map/pois_near_property

- GET /guest/properties_on_sale/random
- GET /guest/properties_on_sale/search
- GET /guest/property_on_sale


## SELLER


- GET /seller/profile_info
- PUT /seller

- GET /seller/sold_properties

- POST /seller/property_on_sale
- PUT /seller/property_on_sale
- DELETE /seller/property_on_sale

- GET /seller/properties_on_sale/reservations
- POST /seller/sell_property_on_sale
- POST /seller/properties_on_sale/search

- POST /seller/analytics/analytics_2
- POST /seller/analytics/analytics_3


## BUYER

- GET /buyer/profile_info
- PUT /buyer

- POST /buyer/favourite
- GET /buyer/favourites
- DELETE /buyer/favourite/{property_on_sale_id}

- GET /buyer/reservations
- POST /buyer/reservation
- DELETE /buyer/reservation/{property_on_sale_id}
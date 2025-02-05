# API full list


## AUTH

- POST /auth/signup/buyer
- POST /auth/signup/seller

- POST /auth/login
- POST /auth/jwt/refresh


## GUEST(non loggati)

- GET /guest/map/get_properties_near_property
- GET /guest/map/get_pois_near_property

- GET /guest/properties_on_sale/random
- GET /guest/properties_on_sale/search
- GET /guest/properties_on_sale


## SELLER


- GET /seller/profile_info
- PUT /seller

- GET /seller/sold_properties

- POST /seller/properties_on_sale
- PUT /seller/properties_on_sale
- DELETE /seller/properties_on_sale

- GET /seller/properties_on_sale/reservations
- POST /seller/sell_properties_on_sale
- POST /seller/search_properties_on_sale

- POST /seller/analytics/analytics_2
- POST /seller/analytics/analytics_3


## BUYER

- GET /buyer/profile_info
- PUT /buyer

- POST /buyer/favourites
- GET /buyer/favourites
- DELETE /buyer/favourites

- POST /buyer/reservations
- GET /buyer/reservations
- DELETE /buyer/reservations
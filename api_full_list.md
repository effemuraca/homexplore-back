# API full list


## GUEST(not logged in)

- GET /guest/properties_on_sale/search
- GET /guest/properties_on_sale/random_properties
- GET /guest/property_on_sale/{property_on_sale_id}

- GET /guest/map/property_on_sale/{property_on_sale_id}
- GET /guest/map/city_and_neighborhood
- GET /guest/map/pois_near_property
- GET /guest/map/properties_near_property


## AUTH

- POST /auth/login
- POST /auth/jwt/refresh

- POST /auth/signup/buyer
- POST /auth/signup/seller

## REGISTERED USER

- POST /registered-user/analytics_1
- POST /registered-user/analytics_4
- POST /registered-user/analytics_5

## BUYER

- GET /buyer/profile_info
- PUT /buyer
- DELETE /buyer

- GET /buyer/favourites
- POST /buyer/favourite
- DELETE /buyer/favourite/{property_on_sale_id}

- GET /buyer/reservations
- POST /buyer/reservation
- DELETE /buyer/reservation/{property_on_sale_id}


## SELLER


- GET /seller/profile_info
- PUT /seller

- GET /seller/properties_on_sale
- GET /seller/sold_properties

- POST /seller/property_on_sale
- PUT /seller/property_on_sale
- DELETE /seller/property_on_sale
- POST /seller/sell_property_on_sale

- GET /seller/current_open_house_events
- GET /seller/property_on_sale/reservations

- POST /seller/analytics/analytics_2
- POST /seller/analytics/analytics_3


## EXTRA - Bulk APIs

- POST /bulk/neo4j
- DELETE /bulk/neo4j
- PUT /bulk/neo4j/score

- POST /bulk/redis
- DELETE /bulk/redis
- GET /bulk/redis/verify

- POST /bulk/mongodb
- DELETE /bulk/mongodb
- GET /bulk/mongodb/verify
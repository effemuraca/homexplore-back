from fastapi import FastAPI
#from modules.Auth.auth_router import auth_router
#from modules.OpenHouse.open_house_router import open_house_router
from modules.ReservationsSeller.reservations_seller_router import reservations_seller_router
from modules.ReservationsBuyer.reservations_buyer_router import reservations_buyer_router
#from modules.OpenHouse.open_house_router import open_house_router
from modules.Buyers.buyers_router import buyers_router
from modules.PropertyOnSale.property_on_sale_router import property_on_sale_router
from modules.Seller.seller_router import seller_router
from modules.KVDBRoutes.kvdb_router import kvdb_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="HomeXplore API",
    description="API for HomeXplore",
    version="0.1",
    docs_url="/",
    redoc_url="/redoc",
    openapi_url="/api/v1/openapi.json",
    debug=True
)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


#app.include_router(auth_router)
#app.include_router(open_house_router)
app.include_router(buyers_router)
app.include_router(property_on_sale_router)
app.include_router(reservations_seller_router)
app.include_router(reservations_buyer_router)
app.include_router(seller_router)
app.include_router(kvdb_router)

# router have to be included after the app is created, here


@app.get("/")
def read_root():
    return {"Hello": "World"}
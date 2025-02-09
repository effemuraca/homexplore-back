from fastapi import FastAPI
from modules.Auth.auth_router import auth_router
from modules.Seller.seller_router import seller_router
from modules.Buyer.buyer_router import buyer_router
from modules.RegisteredUser.registered_user_router import registered_user_router
from modules.Guest.guest_router import guest_router
from bulk.bulk_router import bulk_router
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


app.include_router(guest_router)
app.include_router(auth_router)
app.include_router(registered_user_router)
app.include_router(buyer_router)
app.include_router(seller_router)
app.include_router(bulk_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
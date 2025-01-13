from fastapi import FastAPI
from modules.Auth.auth_router import auth_router
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

# router have to be included after the app is created, here


@app.get("/")
def read_root():
    return {"Hello": "World"}
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from entities.PropertyOnSale.property_on_sale import PropertyOnSale
from entities.PropertyOnSale.db_property_on_sale import PropertyOnSaleDB
from modules.PropertyOnSale.models.property_on_sale_models import CreatePropertyOnSale 

property_on_sale_router = APIRouter(prefix="/properties-on-sale", tags=["PropertiesOnSale"])

# Sistemare per prendere come input non un oggetto ma solo i campi necessari
@property_on_sale_router.post("/")
def create_property_on_sale(property_on_sale: CreatePropertyOnSale):
    property_on_sale = PropertyOnSale(**property_on_sale.model_dump())
    db_property_on_sale = PropertyOnSaleDB(property_on_sale)
    if not db_property_on_sale.create_property_on_sale():
        raise HTTPException(status_code=500, detail="Failed to create property.")
    return JSONResponse(status_code=201, content={"detail": "Property created successfully."})





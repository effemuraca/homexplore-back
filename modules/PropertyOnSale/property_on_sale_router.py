from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from entities.PropertyOnSale.property_on_sale import PropertyOnSale
from entities.PropertyOnSale.db_property_on_sale import PropertyOnSaleDB
from modules.PropertyOnSale.models.property_on_sale_models import CreatePropertyOnSale, UpdatePropertyOnSale

property_on_sale_router = APIRouter(prefix="/properties-on-sale", tags=["PropertiesOnSale"])

@property_on_sale_router.post("/")
def create_property_on_sale(property_on_sale: CreatePropertyOnSale):
    property_on_sale = PropertyOnSale(**property_on_sale.model_dump())
    db_property_on_sale = PropertyOnSaleDB(property_on_sale)
    response = db_property_on_sale.create_property_on_sale()
    if response!=201:
        raise HTTPException(status_code=response, detail="Failed to create property.")
    return JSONResponse(status_code=201, content={"detail": "Property created successfully.", "_id": db_property_on_sale.property_on_sale.property_on_sale_id})

@property_on_sale_router.get("/")
def get_properties_on_sale(property_on_sale_id: str):
    property_on_sale = PropertyOnSale(property_on_sale_id=property_on_sale_id)
    db_property_on_sale = PropertyOnSaleDB(property_on_sale)
    response = db_property_on_sale.get_property_on_sale_by_id()
    if response!=201:
        raise HTTPException(status_code=response, detail="Failed to get property.")
    information=db_property_on_sale.property_on_sale.model_dump()
    information["registration_date"] = information["registration_date"].strftime("%m/%d/%Y, %H:%M:%S")
    del information["property_on_sale_id"]
    return JSONResponse(status_code=201, content={"detail": "Property retrieved successfully.", "informations": information})

@property_on_sale_router.delete("/")
def delete_property_on_sale(property_on_sale_id: str):
    property_on_sale = PropertyOnSale(property_on_sale_id=property_on_sale_id)
    db_property_on_sale = PropertyOnSaleDB(property_on_sale)
    response = db_property_on_sale.delete_property_on_sale_by_id()
    if response!=201:
        raise HTTPException(status_code=response, detail="Failed to delete property.")
    return JSONResponse(status_code=201, content={"detail": "Property deleted successfully."})

@property_on_sale_router.put("/")
def update_property_on_sale(property_on_sale: UpdatePropertyOnSale):
    property_on_sale = PropertyOnSale(**property_on_sale.model_dump())
    db_property_on_sale = PropertyOnSaleDB(property_on_sale)
    response = db_property_on_sale.update_property_on_sale_by_id()
    if response!=201:
        raise HTTPException(status_code=response, detail="Failed to update property.")
    return JSONResponse(status_code=201, content={"detail": "Property updated successfully."})

    



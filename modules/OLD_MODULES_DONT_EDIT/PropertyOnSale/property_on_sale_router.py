from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from entities.MongoDB.PropertyOnSale.property_on_sale import PropertyOnSale
from entities.MongoDB.PropertyOnSale.db_property_on_sale import PropertyOnSaleDB
from modules.PropertyOnSale.models.property_on_sale_models import CreatePropertyOnSale, UpdatePropertyOnSale
from modules.PropertyOnSale.models import response_models as ResponseModels
from typing import List, Optional

property_on_sale_router = APIRouter(prefix="/properties-on-sale", tags=["PropertiesOnSale"])

@property_on_sale_router.post("/", response_model=ResponseModels.CreatePropertyOnSaleResponseModel, responses=ResponseModels.CreatePropertyOnSaleResponses)
def create_property_on_sale(property_on_sale: CreatePropertyOnSale):
    property_on_sale = PropertyOnSale(**property_on_sale.model_dump())
    db_property_on_sale = PropertyOnSaleDB(property_on_sale)
    response = db_property_on_sale.create_property_on_sale()
    if response == 400:
        raise HTTPException(status_code=response, detail="Invalid property information.")
    if response == 500:
        raise HTTPException(status_code=response, detail="Failed to create property.")
    return JSONResponse(status_code=201, content={"detail": "Property created successfully.", "property_id": property_on_sale.property_on_sale_id})

@property_on_sale_router.get("/", response_model=ResponseModels.PropertyOnSale, responses=ResponseModels.GetPropertiesOnSaleResponses)
def get_properties_on_sale(property_on_sale_id: str):
    db_property_on_sale = PropertyOnSaleDB(PropertyOnSale())
    response = db_property_on_sale.get_property_on_sale_by_id(property_on_sale_id)
    if response == 400:
        raise HTTPException(status_code=response, detail="Invalid property id.")
    if response == 404:
        raise HTTPException(status_code=response, detail="Property not found.")
    return db_property_on_sale.property_on_sale

@property_on_sale_router.delete("/", response_model=ResponseModels.SuccessModel, responses=ResponseModels.DeletePropertyOnSaleResponses)
def delete_property_on_sale(property_on_sale_id: str):
    db_property_on_sale = PropertyOnSaleDB(PropertyOnSale())
    response = db_property_on_sale.delete_property_on_sale_by_id(property_on_sale_id)
    if response == 400:
        raise HTTPException(status_code=response, detail="Invalid property id.")
    if response == 404:
        raise HTTPException(status_code=response, detail="Property not found.")
    return JSONResponse(status_code=200, content={"detail": "Property deleted successfully."})

@property_on_sale_router.put("/", response_model=ResponseModels.SuccessModel, responses=ResponseModels.UpdatePropertyOnSaleResponses)
def update_property_on_sale(property_on_sale: UpdatePropertyOnSale):
    property_on_sale = PropertyOnSale(**property_on_sale.model_dump())
    db_property_on_sale = PropertyOnSaleDB(property_on_sale)
    response = db_property_on_sale.update_property_on_sale()
    if response == 400:
        raise HTTPException(status_code=response, detail="Invalid property id.")
    if response == 404:
        raise HTTPException(status_code=response, detail="Property not found.")
    return JSONResponse(status_code=200, content={"detail": "Property updated successfully."})

@property_on_sale_router.get("/search", response_model=List[PropertyOnSale], responses=ResponseModels.GetFilteredPropertiesOnSaleResponses)
def filtered_search(
    city: Optional[str] = None,
    max_price: Optional[int] = None,
    neighbourhood: Optional[str] = None,
    type: Optional[str] = None,
    area: Optional[int] = None,
    min_bed_number: Optional[int] = None,
    min_bath_number: Optional[int] = None
):
    db_property_on_sale = PropertyOnSaleDB(PropertyOnSale())
    result_code = db_property_on_sale.filtered_search(
        city=city if city else "",
        max_price=max_price if max_price is not None else 0,
        neighbourhood=neighbourhood if neighbourhood else "",
        type=type if type else "",
        area=area if area is not None else 0,
        min_bed_number=min_bed_number if min_bed_number is not None else 0,
        min_bath_number=min_bath_number if min_bath_number is not None else 0
    )
    if result_code == 500:
        raise HTTPException(status_code=500, detail="Internal server error.")
    return db_property_on_sale.property_on_sale


@property_on_sale_router.get("/get_random", response_model=List[PropertyOnSale], responses=ResponseModels.GetRandomPropertiesOnSaleResponses)
def get_10_random_properties():
    db_property_on_sale = PropertyOnSaleDB(PropertyOnSale())
    result_code = db_property_on_sale.get_10_random_properties()
    if result_code == 500:
        raise HTTPException(status_code=500, detail="Internal server error.")
    return db_property_on_sale.property_on_sale


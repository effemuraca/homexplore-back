from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from modules.Guest.models import response_models as ResponseModels
from entities.MongoDB.PropertyOnSale.property_on_sale import PropertyOnSale
from entities.MongoDB.PropertyOnSale.db_property_on_sale import PropertyOnSaleDB
from typing import List, Optional

from bson.objectid import ObjectId 
from setup.mongo_setup.mongo_setup import get_default_mongo_db
from datetime import datetime

from modules.Guest.models.guest_models import FilteredSearchInput

guest_router = APIRouter(prefix="/guest", tags=["Guest"])

#CONTROLLATA
#ricerca filtrata
@guest_router.post("/properties_on_sale/search", response_model=List[PropertyOnSale], responses=ResponseModels.GetFilteredPropertiesOnSaleResponses)
def filtered_search(input : FilteredSearchInput):
    db_property_on_sale = PropertyOnSaleDB(PropertyOnSale())
    result_code = db_property_on_sale.filtered_search(input)
    if result_code == 500:
        raise HTTPException(status_code=500, detail="Internal server error.")
    if result_code == 404:
        raise HTTPException(status_code=404, detail="No properties found.")
    return db_property_on_sale.property_on_sale_list

#CONTROLLATA
#ritorna 10 proprietà random
@guest_router.get("/properties_on_sale/get_random", response_model=List[PropertyOnSale], responses=ResponseModels.GetRandomPropertiesOnSaleResponses)
def get_10_random_properties():
    db_property_on_sale = PropertyOnSaleDB(PropertyOnSale())
    result_code = db_property_on_sale.get_10_random_properties()
    if result_code == 500:
        raise HTTPException(status_code=500, detail="Internal server error.")
    if result_code == 404:
        raise HTTPException(status_code=404, detail="No properties found.")
    return db_property_on_sale.property_on_sale_list

#CONTROLLATA
#ricerca singola per id (a che serve al guest?)
@guest_router.get("/property_on_sale", response_model=PropertyOnSale, responses=ResponseModels.GetPropertyOnSaleResponses)
def get_properties_on_sale(property_on_sale_id: str):
    db_property_on_sale = PropertyOnSaleDB(PropertyOnSale())
    response = db_property_on_sale.get_property_on_sale_by_id(property_on_sale_id)
    if response == 400:
        raise HTTPException(status_code=response, detail="Invalid property id.")
    if response == 404:
        raise HTTPException(status_code=response, detail="Property not found.")
    db_property_on_sale.property_on_sale.disponibility = None
    return db_property_on_sale.property_on_sale

#CONTROLLATA
#ricerca per città ed indirizzo
@guest_router.get("/properties_on_sale/search_by_address", response_model=PropertyOnSale, responses=ResponseModels.GetPropertyOnSaleResponses)
def search_by_address(city: str, address: str):
    db_property_on_sale = PropertyOnSaleDB(PropertyOnSale())
    response = db_property_on_sale.search_by_address(city, address)
    if response == 404:
        raise HTTPException(status_code=response, detail="Property not found.")
    db_property_on_sale.property_on_sale.disponibility = None
    return db_property_on_sale.property_on_sale

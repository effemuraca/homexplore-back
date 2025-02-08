from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from modules.Guest.models import response_models as ResponseModels
from entities.MongoDB.PropertyOnSale.property_on_sale import PropertyOnSale
from entities.MongoDB.PropertyOnSale.db_property_on_sale import PropertyOnSaleDB

from entities.Neo4J.PropertyOnSaleNeo4J.property_on_sale_neo4j import PropertyOnSaleNeo4J
from entities.Neo4J.PropertyOnSaleNeo4J.db_property_on_sale_neo4j import PropertyOnSaleNeo4JDB
from entities.Neo4J.City.city import City
from entities.Neo4J.Neighbourhood.neighbourhood import Neighbourhood
from entities.Neo4J.POI.poi import POI
from typing import List, Optional

from bson.objectid import ObjectId 
from setup.mongo_setup.mongo_setup import get_default_mongo_db
from datetime import datetime

from modules.Guest.models.guest_models import FilteredSearchInput

guest_router = APIRouter(prefix="/guest", tags=["Guest"])

#CONSISTENT
@guest_router.post("/properties_on_sale/search", response_model=List[PropertyOnSale], responses=ResponseModels.GetFilteredPropertiesOnSaleResponses)
def filtered_search(input : FilteredSearchInput):
    db_property_on_sale = PropertyOnSaleDB(PropertyOnSale())
    result_code = db_property_on_sale.filtered_search(input)
    if result_code == 500:
        raise HTTPException(status_code=500, detail="Internal server error.")
    if result_code == 404:
        raise HTTPException(status_code=404, detail="No properties found.")
    return db_property_on_sale.property_on_sale_list

#CONSISTENT
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
@guest_router.get("/properties_on_sale/search_by_address", response_model=List[PropertyOnSale], responses=ResponseModels.GetPropertyOnSaleResponses)
def search_by_address(city: str, address: str):
    db_property_on_sale = PropertyOnSaleDB(PropertyOnSale())
    response = db_property_on_sale.get_property_on_sale_by_address(city, address)
    if response == 404:
        raise HTTPException(status_code=response, detail="Property not found.")
    return db_property_on_sale.property_on_sale_list


# Map

@guest_router.get("/map/city_and_neighborhood", response_model= ResponseModels.CityAndNeighbourhood, responses=ResponseModels.GetCityAndNeighbourhoodResponses)
def get_city_and_neighbourhood(property_on_sale_id:str):
    #check validity of property_on_sale_id
    if not ObjectId.is_valid(property_on_sale_id):
        raise HTTPException(status_code=400, detail="Invalid property_on_sale_id.")
    db_property_on_sale_neo4j = PropertyOnSaleNeo4JDB(PropertyOnSaleNeo4J(property_on_sale_id=property_on_sale_id))
    response = db_property_on_sale_neo4j.get_city_and_neighbourhood()
    if response == 404:
        raise HTTPException(status_code=response, detail="Property not found.")
    if response == 500:
        raise HTTPException(status_code=response, detail="Internal server error.")
    
    return ResponseModels.CityAndNeighbourhood(city=db_property_on_sale_neo4j.city, neighbourhood=db_property_on_sale_neo4j.neighbourhood)


@guest_router.get("/map/pois_near_property", response_model=List[POI], responses=ResponseModels.GetPOIsResponses)
def get_pois(property_on_sale_id:str):
    #check validity of property_on_sale_id
    if not ObjectId.is_valid(property_on_sale_id):
        raise HTTPException(status_code=400, detail="Invalid property_on_sale_id.")
    db_property_on_sale_neo4j = PropertyOnSaleNeo4JDB(PropertyOnSaleNeo4J(property_on_sale_id=property_on_sale_id))
    print(db_property_on_sale_neo4j.property_on_sale_neo4j.property_on_sale_id)
    response = db_property_on_sale_neo4j.get_near_POIs()
    if response == 404:
        raise HTTPException(status_code=response, detail="Property not found.")
    if response == 500:
        raise HTTPException(status_code=response, detail="Internal server error.")
    
    return db_property_on_sale_neo4j.pois

@guest_router.get("/map/properties_near_property", response_model=List[PropertyOnSaleNeo4J], responses=ResponseModels.GetNearPropertiesResponses)
def get_near_properties(property_on_sale_id:str):
    #check validity of property_on_sale_id
    if not ObjectId.is_valid(property_on_sale_id):
        raise HTTPException(status_code=400, detail="Invalid property_on_sale_id.")
    db_property_on_sale_neo4j = PropertyOnSaleNeo4JDB(PropertyOnSaleNeo4J(property_on_sale_id=property_on_sale_id))
    response = db_property_on_sale_neo4j.get_near_properties()
    if response == 404:
        raise HTTPException(status_code=response, detail="Property not found.")
    if response == 500:
        raise HTTPException(status_code=response, detail="Internal server error.")
    
    return db_property_on_sale_neo4j.near_properties

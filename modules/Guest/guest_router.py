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
from modules.Guest.models.guest_models import SummaryPropertyOnSale

guest_router = APIRouter(prefix="/guest", tags=["Guest"])

@guest_router.post("/properties_on_sale/search", response_model=List[SummaryPropertyOnSale], responses=ResponseModels.GetFilteredPropertiesOnSaleResponses)
def filtered_search(input: FilteredSearchInput, page: int = 1, page_size: int = 10):
    """
    Search for properties on sale based on input parameters with pagination support.

    Args:
        input (FilteredSearchInput): Filter criteria for the search.
        page (int): Current page number (default is 1).
        page_size (int): Number of results per page (default is 10).

    Raises:
        HTTPException: 500 if there is an internal server error.
                       404 if no properties match the search criteria.

    Returns:
        List[SummaryPropertyOnSale]: The list of properties on sale that match the search criteria, with a summary of each property.
    """
    db_property_on_sale = PropertyOnSaleDB(PropertyOnSale())
    result_code = db_property_on_sale.filtered_search(input, page, page_size)
    if result_code == 500:
        raise HTTPException(status_code=500, detail="Internal server error.")
    if result_code == 404:
        raise HTTPException(status_code=404, detail="No properties found.")
    return db_property_on_sale.property_on_sale_list

@guest_router.get("/properties_on_sale/random_properties", response_model=List[SummaryPropertyOnSale], responses=ResponseModels.GetRandomPropertiesOnSaleResponses)
def get_6_random_properties():
    """
    Get 6 random properties on sale.

    Raises:
        HTTPException: 500 if there is an internal server error.
                       404 if no properties are found.

    Returns:
        List[SummaryPropertyOnSale]: The list of 6 random properties on sale.
    """
    db_property_on_sale = PropertyOnSaleDB(PropertyOnSale())
    result_code = db_property_on_sale.get_6_random_properties()
    if result_code == 500:
        raise HTTPException(status_code=500, detail="Internal server error.")
    if result_code == 404:
        raise HTTPException(status_code=404, detail="No properties found.")
    return db_property_on_sale.property_on_sale_list

@guest_router.get("/property_on_sale/{property_on_sale_id}", response_model=PropertyOnSale, responses=ResponseModels.GetPropertyOnSaleResponses)
def get_property_on_sale(property_on_sale_id:str):
    """
    Get the property on sale with the given ID.

    Args:
        property_on_sale_id (str): The ID of the property on sale.

    Raises:
        HTTPException: 400 if the ID is invalid.
                       404 if the property is not found.
                       500 if there is an internal server error.

    Returns:
        PropertyOnSale: The property on sale with the given ID.
    """
    if not ObjectId.is_valid(property_on_sale_id):
        raise HTTPException(status_code=400, detail="Invalid property_on_sale_id.")
    db_property_on_sale = PropertyOnSaleDB(PropertyOnSale())
    response = db_property_on_sale.get_property_on_sale_by_id(property_on_sale_id)
    if response == 404:
        raise HTTPException(status_code=response, detail="Property not found.")
    if response == 500:
        raise HTTPException(status_code=response, detail="Internal server error.")
    
    return db_property_on_sale.property_on_sale

# Map

@guest_router.get("/map/city_and_neighborhood", response_model= ResponseModels.CityAndNeighbourhood, responses=ResponseModels.GetCityAndNeighbourhoodResponses)
def get_city_and_neighbourhood(property_on_sale_id:str):
    """
    Get the city and neighbourhood of the property on sale with the given ID.

    Args:
        property_on_sale_id (str): The ID of the property on sale.

    Raises:
        HTTPException: 400 if the ID is invalid.
                       404 if the property is not found.
                       500 if there is an internal server error.

    Returns:
        CityAndNeighbourhood: The city and neighbourhood of the property on sale.
    """
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
    """
    Get the points of interest near the property on sale with the given ID.

    Args:
        property_on_sale_id (str): The ID of the property on sale.

    Raises:
        HTTPException: 400 if the ID is invalid.
                       404 if the property is not found.
                       500 if there is an internal server error.

    Returns:
        List[POI]: The points of interest near the property on sale.
    """
    if not ObjectId.is_valid(property_on_sale_id):
        raise HTTPException(status_code=400, detail="Invalid property_on_sale_id.")
    db_property_on_sale_neo4j = PropertyOnSaleNeo4JDB(PropertyOnSaleNeo4J(property_on_sale_id=property_on_sale_id))
    response = db_property_on_sale_neo4j.get_near_POIs()
    if response == 404:
        raise HTTPException(status_code=response, detail="POIs or property not found.")
    if response == 500:
        raise HTTPException(status_code=response, detail="Internal server error.")
    
    return db_property_on_sale_neo4j.pois

@guest_router.get("/map/properties_near_property", response_model=List[PropertyOnSaleNeo4J], responses=ResponseModels.GetNearPropertiesResponses)
def get_near_properties(property_on_sale_id:str):
    """
    Get the properties near the property on sale with the given ID.

    Args:
        property_on_sale_id (str): The ID of the property on sale.

    Raises:
        HTTPException: 400 if the ID is invalid.
                       404 if the property is not found.
                       500 if there is an internal server error.

    Returns:
        List[PropertyOnSaleNeo4J]: The properties near the property on sale.
    """
    if not ObjectId.is_valid(property_on_sale_id):
        raise HTTPException(status_code=400, detail="Invalid property_on_sale_id.")
    db_property_on_sale_neo4j = PropertyOnSaleNeo4JDB(PropertyOnSaleNeo4J(property_on_sale_id=property_on_sale_id))
    response = db_property_on_sale_neo4j.get_near_properties()
    if response == 404:
        raise HTTPException(status_code=response, detail="Property not found.")
    if response == 500:
        raise HTTPException(status_code=response, detail="Internal server error.")
    
    return db_property_on_sale_neo4j.near_properties

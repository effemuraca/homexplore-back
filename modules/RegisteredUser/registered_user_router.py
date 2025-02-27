from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from entities.MongoDB.PropertyOnSale.db_property_on_sale import PropertyOnSaleDB
from modules.RegisteredUser.models.registered_user_models import Analytics1Input
from modules.RegisteredUser.models import response_models as ResponseModels

from modules.Auth.helpers.JwtHandler import JWTHandler

registered_user_router = APIRouter(prefix="/registered-user", tags=["RegisteredUser"])


@registered_user_router.post("/analytics_1", response_model=ResponseModels.Analytics1ResponseModel, responses=ResponseModels.Analytics1Responses)
def analytics_1(input: Analytics1Input, access_token: str = Depends(JWTHandler())):
    """
    Given the input parameters, return the average price per square meter for each neighbourhood in the city, if "type" is specified filters the results by the property type, if "order_by" is specified orders the results consequently.

    Authorization: 
        access_token (str): The JWT access token for authentication.
    
    Body:
        (Analytics1Input): The input parameters for the analytics.

    Raises:
        HTTPException: 401 if the access token is invalid.
                       500 if there is an internal server error.
                       404 if no data is found.

    Returns:
        JSONResponse: The response containing the analytics result.
    """
    user_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    property_on_sale_db = PropertyOnSaleDB()
    status = property_on_sale_db.get_avg_price_per_square_meter(input)
    
    if status == 500:
        raise HTTPException(status_code=500, detail="Internal server error")
    elif status == 404:
        raise HTTPException(status_code=404, detail="No data found")
    else:
        return JSONResponse(status_code=200,content={"detail": "Data found successfully", "result": property_on_sale_db.analytics_1_result})

@registered_user_router.post("/analytics_4", response_model=ResponseModels.Analytics4ResponseModel, responses=ResponseModels.Analytics4Responses)
def analytics_4(city: str, access_token: str = Depends(JWTHandler())):
    """
    Given the city, return the average price per square meter and the number of properties for each property type.

    Args:
        city (str): The city to analyze.

    Authorization: access_token (str): The JWT access token for authentication.

    Raises:
        HTTPException: 401 if the access token is invalid.
                       500 if there is an internal server error.
                       404 if no data is found.

    Returns:
        JSONResponse: The response containing the analytics result.
    """
    user_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    property_on_sale_db = PropertyOnSaleDB()
    status = property_on_sale_db.get_avg_price_per_square_meter_by_city(city)
    
    if status == 500:
        raise HTTPException(status_code=500, detail="Internal server error")
    elif status == 404:
        raise HTTPException(status_code=404, detail="No data found")
    else:
        return JSONResponse(status_code=200,content={"detail": "Data found successfully", "result": property_on_sale_db.analytics_4_result})

@registered_user_router.post("/analytics_5", response_model=ResponseModels.Analytics5ResponseModel, responses=ResponseModels.Analytics5Responses)
def analytics_5(city: str, neighbourhood: str, access_token: str = Depends(JWTHandler())):
    """
    Given the city and neighbourhood, return the average bed_number, bath_number, and area for each property type.

    Args:
        city (str): The city to analyze.    
        neighbourhood (str): The neighbourhood to analyze.  

    Authorization: access_token (str): The JWT access token for authentication.

    Raises:
        HTTPException: 401 if the access token is invalid.
                       500 if there is an internal server error.
                       404 if no data is found.

    Returns:
        JSONResponse: The response containing the analytics result.
    """
    user_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    property_on_sale_db = PropertyOnSaleDB()
    status = property_on_sale_db.get_statistics_by_city_and_neighbourhood(city, neighbourhood)
    
    if status == 500:
        raise HTTPException(status_code=500, detail="Internal server error")
    elif status == 404:
        raise HTTPException(status_code=404, detail="No data found")
    else:
        return JSONResponse(status_code=200,content={"detail": "Data found successfully", "result": property_on_sale_db.analytics_5_result})










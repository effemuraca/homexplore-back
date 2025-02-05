from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from entities.MongoDB.Seller.seller import Seller
from entities.MongoDB.Seller.db_seller import SellerDB
from modules.Seller.models.seller_models import UpdateSeller
from modules.Seller.models import response_models as ResponseModels
from entities.Redis.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS
from entities.Redis.ReservationsSeller.db_reservations_seller import ReservationsSellerDB
from entities.MongoDB.PropertyOnSale.property_on_sale import PropertyOnSale
from entities.MongoDB.PropertyOnSale.db_property_on_sale import PropertyOnSaleDB
from modules.Seller.models.seller_models import CreatePropertyOnSale, UpdatePropertyOnSale
from modules.Seller.models.seller_models import Analytics2Input, Analytics3Input, Analytics6Input
from typing import List, Optional
from bson.objectid import ObjectId

from setup.mongo_setup.mongo_setup import get_default_mongo_db
from datetime import datetime

from modules.Auth.helpers.auth_helpers import JWTHandler, hash_password
import logging

seller_router = APIRouter(prefix="/seller", tags=["Seller"])

# Configura il logger
logger = logging.getLogger(__name__)

#Seller

@seller_router.get("/profile_info", response_model=Seller, responses=ResponseModels.GetSellerResponses)
def get_seller(access_token: str = Depends(JWTHandler())):
    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    temp_seller = Seller(seller_id=seller_id)
    db_seller = SellerDB(temp_seller)
    response = db_seller.get_profile_info()
    if response == 400:
        raise HTTPException(status_code=400, detail="Invalid seller id")
    if response == 404:
        raise HTTPException(status_code=404, detail="Seller not found.")
    return db_seller.seller

@seller_router.put("/", response_model=ResponseModels.SuccessModel, responses=ResponseModels.UpdateSellerResponses)
def update_seller(seller: UpdateSeller, access_token: str = Depends(JWTHandler())):
    """
    Updates an existing seller.
    """
    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    seller_old = Seller(seller_id=seller_id)
    seller_db = SellerDB(seller_old)
    result = seller_db.get_profile_info()
    if result == 404:
        raise HTTPException(status_code=result, detail="Seller not found.")
    
    if seller.email:
        seller_db.get_seller_by_email(seller.email)
        if seller_db.seller and seller_db.seller.seller_id != seller_id:
            raise HTTPException(status_code=409, detail="Email already exists.")
    
    # check if there's a password to crypt
    if seller.password:
        seller.password = hash_password(seller.password)
    
    result = seller_db.update_seller(seller)
    if result == 400:
        raise HTTPException(status_code=result, detail="Seller ID is required.")
    elif result == 404:
        raise HTTPException(status_code=result, detail="Seller not found.")
    elif result == 500:
        raise HTTPException(status_code=result, detail="Failed to update seller.")
    elif result == 200:
        return JSONResponse(status_code=result, content={"detail": "Seller updated successfully."})

@seller_router.get("/sold_properties", response_model=Seller, responses=ResponseModels.GetSoldPropertiesByPriceDescResponses)
def get_sold_properties_by_price_desc():
    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    db_seller = SellerDB()
    result = db_seller.get_sold_properties_by_price_desc(seller_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="Seller not found.")
    if result == 500:
        raise HTTPException(status_code=500, detail="Failed to retrieve sold properties.")
    return db_seller.seller


# Properties on sale

@seller_router.post("/property_on_sale", response_model=ResponseModels.CreatePropertyOnSaleResponseModel, responses=ResponseModels.CreatePropertyOnSaleResponses)
def create_property_on_sale(property_on_sale: CreatePropertyOnSale, access_token: str = Depends(JWTHandler())):
    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    # TODO: BISOGNA AGGIUNGERE LA PROPERTY DOVE SERVE, DA TUTTE LE PARTI, CON QUERY SEPARATE
    
    property_on_sale = PropertyOnSale(**property_on_sale.model_dump())
    db_property_on_sale = PropertyOnSaleDB(property_on_sale)
    response = db_property_on_sale.create_property_on_sale()
    if response == 400: #non facciamo nessun controllo sui campi, quindi non dovrebbe mai accadere
        raise HTTPException(status_code=response, detail="Invalid property information.")
    if response == 500:
        raise HTTPException(status_code=response, detail="Failed to create property.")
    return JSONResponse(status_code=201, content={"detail": "Property created successfully.", "property_id": property_on_sale.property_on_sale_id})

@seller_router.put("/property_on_sale", response_model=ResponseModels.SuccessModel, responses=ResponseModels.UpdatePropertyOnSaleResponses)
def update_property_on_sale(property_on_sale: UpdatePropertyOnSale, access_token: str = Depends(JWTHandler())):
    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    # TODO: BISOGNA MODIFICARE LA ROBA DOVE SERVE, DA TUTTE LE PARTI, CON QUERY SEPARATE
    
    property_on_sale = PropertyOnSale(**property_on_sale.model_dump())
    db_property_on_sale = PropertyOnSaleDB(property_on_sale)
    response = db_property_on_sale.update_property_on_sale()
    if response == 400:
        raise HTTPException(status_code=response, detail="Invalid property id.")
    if response == 404:
        raise HTTPException(status_code=response, detail="Property not found.")
    return JSONResponse(status_code=200, content={"detail": "Property updated successfully."})

# Finire di controllare
# sell a property 
# (move it from properties_on_sale to sold_properties of the seller & delete it from the property_on_sale collection)
@seller_router.post("/sell_property_on_sale", response_model=ResponseModels.SuccessModel)
def sell_property(property_to_sell_id: str, access_token: str = Depends(JWTHandler())):
    if ObjectId.is_valid(property_to_sell_id) is False:
        raise HTTPException(status_code=400, detail="Invalid property id.")
    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    # TODO: BISOGNA MODIFICARE LA ROBA DOVE SERVE, DA TUTTE LE PARTI, CON QUERY SEPARATE
    
    db_entity = SellerDB(Seller())
    result = db_entity.db_sell_property(property_to_sell_id, seller_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="Property not found.")
    if result == 500:
        raise HTTPException(status_code=500, detail="Failed to sell property.")
    return JSONResponse(status_code=200, content={"detail": "Property sold successfully."})


@seller_router.delete("/property_on_sale", response_model=ResponseModels.SuccessModel, responses=ResponseModels.DeletePropertyOnSaleResponses)
def delete_property_on_sale(property_on_sale_id: str, access_token: str = Depends(JWTHandler())):
    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    # TODO: BISOGNA MODIFICARE LA ROBA DOVE SERVE, DA TUTTE LE PARTI, CON QUERY SEPARATE
    
    db_property_on_sale = PropertyOnSaleDB(PropertyOnSale())
    response = db_property_on_sale.delete_property_on_sale_by_id(property_on_sale_id)
    if response == 400:
        raise HTTPException(status_code=response, detail="Invalid property id.")
    if response == 404:
        raise HTTPException(status_code=response, detail="Property not found.")
    return JSONResponse(status_code=200, content={"detail": "Property deleted successfully."})


@seller_router.get("/properties_on_sale/search", response_model=List[PropertyOnSale], responses=ResponseModels.GetFilteredPropertiesOnSaleResponses)
def filtered_search(
    city: Optional[str] = None,
    max_price: Optional[int] = None,
    neighbourhood: Optional[str] = None,
    type: Optional[str] = None,
    area: Optional[int] = None,
    min_bed_number: Optional[int] = None,
    min_bath_number: Optional[int] = None,
    access_token: str = Depends(JWTHandler())
):
    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    # TODO: BISOGNA RENDERE QUESTA QUERY FILTRATA PER IL SELLER
    
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

# ReservationsSeller

@seller_router.get(
    "/reservations",
    response_model=ReservationsSeller,
    responses=ResponseModels.GetReservationsSellerResponseModelResponses
)
def get_reservations_seller(property_on_sale_id: str, access_token: str = Depends(JWTHandler())):
    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if not property_on_sale_id:
        raise HTTPException(status_code=400, detail="Property on sale ID is required.")
    reservations_seller = ReservationsSeller(property_on_sale_id=property_on_sale_id)
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    status = reservations_seller_db.get_reservation_seller()
    if status == 404:
        raise HTTPException(status_code=404, detail="No reservations found.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to fetch reservations.")
    return reservations_seller_db.reservations_seller

# Analytics routes

@seller_router.post("/Analytics/Analytics 2", response_model=ResponseModels.AnalyticsResponseModel, responses=ResponseModels.Analytics2Responses)
def analytics_2(input : Analytics2Input, access_token: str = Depends(JWTHandler())):
    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    # TODO: DEVI TOGLIERE IL SELLER_ID DALL'INPUT, E METTERCI QUELLO CHE TI DO IO
    
    mongo_client = get_default_mongo_db()
    if mongo_client is None:
        raise HTTPException(status_code=500, detail="Database client not found")
    #convert input dates into datetime objects
    start = datetime.strptime(input.start_date, "%Y-%m-%d")
    end = datetime.strptime(input.end_date, "%Y-%m-%d")
    #check if the start date is before the end date
    if start > end:
        raise HTTPException(status_code=400, detail="Start date must be before end date")
    try:
        pipeline = [
            {
                "$match": {
                    "_id": ObjectId(input.agency_id),
                }
            },
            {"$unwind": "$sold_properties"},
            {
                "$match": {
                    "sold_properties.city": input.city,
                    "sold_properties.sell_date": {"$gte": start,"$lte": end}
                }
            },
            {
                "$group": {
                    "_id": "$sold_properties.neighbourhood",
                    "houses_sold": {"$sum": 1},
                    "revenue": {"$sum": "$sold_properties.price"}
                }
            }
        ]
        aggregation_result = mongo_client.Seller.aggregate(pipeline)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    aggregation_result = list(aggregation_result)
    if not aggregation_result:
        response="No data found"
    else:
        response="Aggregated data finished successfully"
    return JSONResponse(status_code=200,content={"detail": response, "result": aggregation_result})

@seller_router.post("/Analytics/Analytics 3", response_model=ResponseModels.AnalyticsResponseModel, responses=ResponseModels.Analytics3Responses)
def analytics_3(input : Analytics3Input, access_token: str = Depends(JWTHandler())):
    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    # TODO: DEVI TOGLIERE IL SELLER_ID DALL'INPUT, E METTERCI QUELLO CHE TI DO IO
    
    mongo_client = get_default_mongo_db()
    if mongo_client is None:
        raise HTTPException(status_code=500, detail="Database client not found")
    start=datetime.strptime(input.start_date, "%Y-%m-%d")
    try:
        pipeline = [
            {"$match": {"_id": ObjectId(input.agency_id)}},
            {"$unwind": "$sold_properties"},
            {"$match": {"sold_properties.city": input.city, "sold_properties.registration_date": {"$gte": start}}},
            {"$project": {
                "time_to_sell": {
                    "$divide": [{"$subtract": ["$sold_properties.sell_date", "$sold_properties.registration_date"]},86400000 ]
                },
                "sold_properties.neighbourhood": 1
            }
            },
            {
            "$group": {
                "_id": "$sold_properties.neighbourhood",
                "avg_time_to_sell": {"$avg": "$time_to_sell"},
                "num_house": {"$sum": 1}
            }    
            }
        ]
        aggregation_result = mongo_client.Seller.aggregate(pipeline)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    aggregation_result = list(aggregation_result)
    if not aggregation_result:
        response="No data found"
    else:
        response="Aggregated data finished successfully"
    return JSONResponse(status_code=200,content={"detail": response, "result": aggregation_result})



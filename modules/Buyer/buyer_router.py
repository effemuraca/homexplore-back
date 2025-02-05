from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
import logging
import json
from entities.MongoDB.Buyer.buyer import Buyer, FavouriteProperty
from bson import ObjectId
from entities.MongoDB.Buyer.db_buyer import BuyerDB
from modules.Buyer.models import response_models as ResponseModels
from modules.Buyer.models.buyer_models import UpdateBuyer
from entities.Redis.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB
from entities.Redis.ReservationsBuyer.db_reservations_buyer import ReservationsBuyerDB
from modules.Buyer.models import response_models as ResponseModels
from modules.Buyer.models.buyer_models import CreateReservationBuyer, UpdateReservationBuyer
from modules.Auth.helpers.auth_helpers import JWTHandler, hash_password

buyer_router = APIRouter(prefix="/buyer", tags=["Buyer"])

# Configura il logger
logger = logging.getLogger(__name__)


# Buyer

@buyer_router.get("/profile_info", response_model=Buyer, responses=ResponseModels.GetBuyerResponseModelResponses)
def get_buyer(access_token: str = Depends(JWTHandler())):
    """
    Retrieves a buyer by id.
    """
    buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if buyer_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "buyer":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    buyer_db = BuyerDB()
    result = buyer_db.get_contact_info(buyer_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="Buyer not found.")
    elif result == 400:
        raise HTTPException(status_code=400, detail="Invalid buyer ID.")
    elif result == 500:
        raise HTTPException(status_code=500, detail="Internal server error.")
    return buyer_db.buyer

# @buyer_router.post("/", response_model=ResponseModels.CreateBuyerResponseModel, responses=ResponseModels.CreateBuyerResponseModelResponses)
# def create_buyer(buyer: CreateBuyer):
#     """
#     Creates a new buyer.
#     """
#     if not buyer:
#         raise HTTPException(status_code=400, detail="Missing buyer info.")
    
#     buyer_db = BuyerDB(Buyer(**buyer.dict()))
#     result = buyer_db.create_buyer()
#     if result == 400:
#         raise HTTPException(status_code=result, detail="Invalid buyer info.")
#     elif result == 500:
#         raise HTTPException(status_code=result, detail="Failed to create buyer.")
#     elif result == 201:
#         return JSONResponse(status_code=201, content={"detail": "Buyer created successfully.", "buyer_id": buyer_db.buyer.buyer_id})

@buyer_router.put("/", response_model=ResponseModels.SuccessModel, responses=ResponseModels.UpdateBuyerResponseModelResponses)
def update_buyer(buyer: UpdateBuyer, access_token: str = Depends(JWTHandler())):
    """
    Updates an existing buyer.
    """
    buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if buyer_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    if user_type != "buyer":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    buyer_db = BuyerDB()
    result = buyer_db.get_contact_info(buyer_id)
    if result == 404:
        raise HTTPException(status_code=result, detail="Buyer not found.")
    
    if buyer.email:
        buyer_db.get_buyer_by_email(buyer.email)
        if buyer_db.buyer and buyer_db.buyer.buyer_id != buyer_id:
            raise HTTPException(status_code=409, detail="Email already exists.")
    
    # check if there's a password to crypt
    if buyer.password:
        buyer.password = hash_password(buyer.password)
    
    result = buyer_db.update_buyer(buyer)
    if result == 400:
        raise HTTPException(status_code=result, detail="Buyer ID is required.")
    elif result == 404:
        raise HTTPException(status_code=result, detail="Buyer not found.")
    elif result == 500:
        raise HTTPException(status_code=result, detail="Failed to update buyer.")
    elif result == 200:
        return JSONResponse(status_code=result, content={"detail": "Buyer updated successfully."})

# @buyer_router.delete("/{buyer_id}", response_model=ResponseModels.SuccessModel, responses=ResponseModels.DeleteBuyerResponseModelResponses)
# def delete_buyer(buyer_id: str):
#     """
#     Deletes a buyer by id.
#     """
#     buyer_db = BuyerDB()
#     result = buyer_db.delete_buyer_by_id(buyer_id)
#     if result == 400:
#         raise HTTPException(status_code=result, detail="Buyer ID is required.")
#     elif result == 404:
#         raise HTTPException(status_code=result, detail="Buyer not found.")
#     elif result == 200:
#         return JSONResponse(status_code=result, content={"detail": "Buyer deleted successfully."})

# Favourites

@buyer_router.get("/favourites", response_model=List[FavouriteProperty], responses=ResponseModels.GetFavouritesResponseModelResponses)
def get_favourites(access_token: str = Depends(JWTHandler())):
    """
    Retrieves the favourite properties of a buyer by id.
    """
    buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if buyer_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "buyer":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    buyer_db = BuyerDB()
    favourites = buyer_db.get_favourites(buyer_id)
    if favourites is None:
        raise HTTPException(status_code=404, detail="Favourites not found.")
    return favourites

@buyer_router.post("/favourites", response_model=ResponseModels.SuccessModel, responses=ResponseModels.AddFavouriteResponseModelResponses)
def add_favourite(favourite: FavouriteProperty, access_token: str = Depends(JWTHandler())):
    """
    Adds a favourite property for a buyer.
    """
    buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if buyer_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "buyer":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    buyer_db = BuyerDB()
    result = buyer_db.add_favourite(buyer_id, favourite)
    if result == 400:
        raise HTTPException(status_code=result, detail="Invalid input.")
    elif result == 500:
        raise HTTPException(status_code=result, detail="Failed to add favourite.")
    elif result == 200:
        return JSONResponse(status_code=result, content={"detail": "Favourite added successfully."})

@buyer_router.delete("/favourites/{property_on_sale_id}", response_model=ResponseModels.SuccessModel, responses=ResponseModels.DeleteFavouriteResponseModelResponses)
def delete_favourite(property_on_sale_id: str, access_token: str = Depends(JWTHandler())):
    """
    Deletes a favourite property for a buyer.
    """
    if not ObjectId.is_valid(property_on_sale_id):
        raise HTTPException(status_code=400, detail="Invalid input.")
    buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if buyer_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "buyer":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    buyer_db = BuyerDB()
    result = buyer_db.delete_favourite(buyer_id, property_on_sale_id)
    if result == 400:
        raise HTTPException(status_code=result, detail="Invalid input.")
    elif result == 500:
        raise HTTPException(status_code=result, detail="Failed to delete favourite.")
    elif result == 200:
        return JSONResponse(status_code=result, content={"detail": "Favourite deleted successfully."})

# @buyer_router.put("/{buyer_id}/favourites/{property_id}", response_model=ResponseModels.SuccessModel, responses=ResponseModels.UpdateFavouriteResponseModelResponses)
# def update_favourite(buyer_id: str, property_id: str, favourite: FavouriteProperty):
#     """
#     Updates a favourite property for a buyer.
#     """
#     buyer_db = BuyerDB()
#     result = buyer_db.update_favourite(buyer_id, property_id, favourite.dict())
#     if result == 400:
#         raise HTTPException(status_code=result, detail="Invalid input.")
#     elif result == 500:
#         raise HTTPException(status_code=result, detail="Failed to update favourite.")
#     elif result == 200:
#         return JSONResponse(status_code=result, content={"detail": "Favourite updated successfully."})


# ReservationsBuyer

@@buyer_router.post(
    "/reservations",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.CreateReservationBuyerResponseModelResponses
)
def create_reservation_buyer(reservations_buyer_info: CreateReservationBuyer, access_token: str = Depends(JWTHandler())):
    try:
        if not reservations_buyer_info:
            raise HTTPException(status_code=400, detail="Missing reservation info.")
        try:
            buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
        except Exception as token_err:
            logger.error(f"Token verification error: {token_err}")
            raise HTTPException(status_code=401, detail="Invalid access token")
        
        if user_type != "buyer":
            raise HTTPException(status_code=401, detail="Invalid access token")
        if buyer_id is None:
            raise HTTPException(status_code=401, detail="Invalid access token")
        if buyer_id != reservations_buyer_info.buyer_id:
            raise HTTPException(status_code=401, detail="Invalid buyer_id")
        
        reservations_buyer = ReservationsBuyer(
            buyer_id=buyer_id,
            reservations=[
                ReservationB(
                    property_on_sale_id=reservations_buyer_info.property_on_sale_id,
                    date=reservations_buyer_info.date,
                    time=reservations_buyer_info.time,
                    thumbnail=reservations_buyer_info.thumbnail,
                    address=reservations_buyer_info.address
                )
            ]
        )
        reservations_buyer_db = ReservationsBuyerDB(reservations_buyer)
        try:
            status = reservations_buyer_db.create_reservation_buyer()
        except Exception as db_err:
            logger.error(f"Error creating buyer reservation: {db_err}")
            raise HTTPException(status_code=500, detail="Error creating buyer reservation")
        
        if status == 409:
            raise HTTPException(status_code=409, detail="Reservation already exists.")
        if status == 500:
            raise HTTPException(status_code=500, detail="Failed to create reservation.")
        
        return JSONResponse(status_code=201, content={"detail": "Buyer reservation created successfully."})
    except Exception as e:
        logger.error(f"Unhandled error in create_reservation_buyer: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

# @buyer_router.get(
#     "/reservations/{buyer_id}",
#     response_model=ReservationsBuyer,
#     responses=ResponseModels.GetReservationsBuyerResponseModelResponses
# )
# def get_reservations_buyer(buyer_id: str):
#     reservations_buyer = ReservationsBuyer(buyer_id=buyer_id, reservations=[])
#     reservations_buyer_db = ReservationsBuyerDB(reservations_buyer)
#     try:
#         status = reservations_buyer_db.get_reservations_by_user()

#     except Exception as e:
#         logger.error(f"Error retrieving buyer reservations: {e}")
#         raise HTTPException(status_code=500, detail="Error retrieving buyer reservations")
    
#     if status == 404:
#         raise HTTPException(status_code=404, detail="No reservations found for buyer.")
#     if status == 500:
#         raise HTTPException(status_code=500, detail="Failed to retrieve reservations.")
    
#     return reservations_buyer_db.reservations_buyer

@buyer_router.put(
    "/reservations",
    response_model=ReservationsBuyer,
    responses=ResponseModels.UpdateReservationsBuyerResponseModelResponses
)
def update_reservations_buyer(reservations_buyer_info: UpdateReservationBuyer, access_token: str = Depends(JWTHandler())):
    try:
        try:
            buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
        except Exception as token_err:
            logger.error(f"Token verification error: {token_err}")
            raise HTTPException(status_code=401, detail="Invalid access token")
        
        if user_type != "buyer":
            raise HTTPException(status_code=401, detail="Invalid access token")
        if buyer_id is None:
            raise HTTPException(status_code=401, detail="Invalid access token")
        if buyer_id != reservations_buyer_info.buyer_id:
            raise HTTPException(status_code=401, detail="Invalid buyer_id")
        
        reservations_buyer = ReservationsBuyer(
            buyer_id=buyer_id,
            reservations=[
                ReservationB(
                    property_on_sale_id=reservations_buyer_info.property_on_sale_id,
                    date=reservations_buyer_info.date,
                    time=reservations_buyer_info.time,
                    thumbnail=reservations_buyer_info.thumbnail,
                    address=reservations_buyer_info.address
                )
            ]
        )
        reservations_buyer_db = ReservationsBuyerDB(reservations_buyer)
        try:
            status = reservations_buyer_db.update_reservation_buyer()
        except Exception as db_err:
            logger.error(f"Error updating buyer reservations: {db_err}")
            raise HTTPException(status_code=500, detail="Error updating buyer reservations")
        
        if status == 404:
            raise HTTPException(status_code=404, detail="Reservation not found.")
        if status == 400:
            raise HTTPException(status_code=400, detail="Invalid input data.")
        if status == 500:
            raise HTTPException(status_code=500, detail="Failed to update reservation.")
        
        return reservations_buyer_db.reservations_buyer
    except Exception as e:
        logger.error(f"Unhandled error in update_reservations_buyer: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

# @buyer_router.delete(
#     "/reservations/{buyer_id}",
#     response_model=ResponseModels.SuccessModel,
#     responses=ResponseModels.DeleteReservationsBuyerResponseModelResponses
# )
# def delete_reservations_buyer(buyer_id: str):
#     reservations_buyer = ReservationsBuyer(buyer_id=buyer_id, reservations=[])
#     reservations_buyer_db = ReservationsBuyerDB(reservations_buyer)
#     try:
#         status = reservations_buyer_db.delete_reservations_buyer()
#     except Exception as e:
#         logger.error(f"Error deleting buyer reservations: {e}")
#         raise HTTPException(status_code=500, detail="Error deleting buyer reservations")

#     if status == 404:
#         raise HTTPException(status_code=404, detail="No reservations found or delete failed.")
#     if status == 500:
#         raise HTTPException(status_code=500, detail="Failed to delete reservation.")
    
#     return JSONResponse(status_code=200, content={"detail": "Buyer reservations deleted successfully."})

@buyer_router.delete(
    "/reservations/{property_on_sale_id}",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.DeleteReservationsBuyerResponseModelResponses
)
def delete_reservation_buyer(property_on_sale_id: str, access_token: str = Depends(JWTHandler())):
    try:
        # Verifica dell'input: se l'ID è valido, potrebbe essere un errore nella logica (o invertire la condizione)
        if ObjectId.is_valid(property_on_sale_id):
            raise HTTPException(status_code=400, detail="Invalid input.")
        
        try:
            buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
        except Exception as token_err:
            logger.error(f"Token verification error: {token_err}")
            raise HTTPException(status_code=401, detail="Invalid access token")
        
        if user_type != "buyer":
            raise HTTPException(status_code=401, detail="Invalid access token")
        if buyer_id is None:
            raise HTTPException(status_code=401, detail="Invalid access token")
        
        reservations_buyer = ReservationsBuyer(buyer_id=buyer_id, reservations=[])
        reservations_buyer_db = ReservationsBuyerDB(reservations_buyer)
        try:
            status = reservations_buyer_db.delete_reservation_by_property_on_sale_id(property_on_sale_id)
        except Exception as db_err:
            logger.error(f"Error deleting buyer reservation: {db_err}")
            raise HTTPException(status_code=500, detail="Error deleting buyer reservation")
        
        if status == 404:
            raise HTTPException(status_code=404, detail="Reservation not found or delete failed.")
        if status == 500:
            raise HTTPException(status_code=500, detail="Failed to delete reservation.")
        
        return JSONResponse(status_code=200, content={"detail": "Buyer reservation deleted successfully."})
    except Exception as e:
        logger.error(f"Unhandled error in delete_reservation_buyer: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

# Analytics


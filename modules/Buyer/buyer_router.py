from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
import logging
import json
from entities.MongoDB.Buyer.buyer import Buyer, FavouriteProperty
from entities.MongoDB.Buyer.db_buyer import BuyerDB
from modules.Buyer.models import response_models as ResponseModels
from entities.Redis.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB
from entities.Redis.ReservationsBuyer.db_reservations_buyer import ReservationsBuyerDB
from modules.Buyer.models import response_models as ResponseModels
from modules.Buyer.models.buyer_models import CreateReservationBuyer, UpdateReservationBuyer
from modules.Auth.helpers.auth_helpers import JWTHandler

buyer_router = APIRouter(prefix="/buyer", tags=["Buyer"])

# Configura il logger
logger = logging.getLogger(__name__)


# Buyer

@buyer_router.get("/{buyer_id}/get_profile_info", response_model=Buyer, responses=ResponseModels.GetBuyerResponseModelResponses)
def get_buyer(buyer_id: str):
    """
    Retrieves a buyer by id.
    """
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
def update_buyer(buyer: Buyer):
    """
    Updates an existing buyer.
    """
    buyer_db = BuyerDB()
    result = buyer_db.get_contact_info(buyer.buyer_id)
    if result == 404:
        raise HTTPException(status_code=result, detail="Buyer not found.")
    
    result = buyer_db.update_buyer(buyer)
    if result == 400:
        raise HTTPException(status_code=result, detail="Buyer ID is required.")
    elif result == 404:
        raise HTTPException(status_code=result, detail="Buyer not found.")
    elif result == 500:
        raise HTTPException(status_code=result, detail="Failed to update buyer.")
    elif result == 200:
        return JSONResponse(status_code=result, content={"detail": "Buyer updated successfully."})

@buyer_router.delete("/{buyer_id}", response_model=ResponseModels.SuccessModel, responses=ResponseModels.DeleteBuyerResponseModelResponses)
def delete_buyer(buyer_id: str):
    """
    Deletes a buyer by id.
    """
    buyer_db = BuyerDB()
    result = buyer_db.delete_buyer_by_id(buyer_id)
    if result == 400:
        raise HTTPException(status_code=result, detail="Buyer ID is required.")
    elif result == 404:
        raise HTTPException(status_code=result, detail="Buyer not found.")
    elif result == 200:
        return JSONResponse(status_code=result, content={"detail": "Buyer deleted successfully."})

# Favourites

@buyer_router.get("/{buyer_id}/favorites", response_model=List[FavouriteProperty], responses=ResponseModels.GetFavoritesResponseModelResponses)
def get_favorites(buyer_id: str):
    """
    Retrieves the favorite properties of a buyer by id.
    """
    buyer_db = BuyerDB()
    favorites = buyer_db.get_favorites(buyer_id)
    if favorites is None:
        raise HTTPException(status_code=404, detail="Favorites not found.")
    return favorites

@buyer_router.post("/{buyer_id}/favorites", response_model=ResponseModels.SuccessModel, responses=ResponseModels.AddFavoriteResponseModelResponses)
def add_favorite(buyer_id: str, favorite: FavouriteProperty):
    """
    Adds a favorite property for a buyer.
    """
    buyer_db = BuyerDB()
    result = buyer_db.add_favorite(buyer_id, favorite)
    if result == 400:
        raise HTTPException(status_code=result, detail="Invalid input.")
    elif result == 500:
        raise HTTPException(status_code=result, detail="Failed to add favorite.")
    elif result == 200:
        return JSONResponse(status_code=result, content={"detail": "Favorite added successfully."})

@buyer_router.delete("/{buyer_id}/favorites/{property_id}", response_model=ResponseModels.SuccessModel, responses=ResponseModels.DeleteFavoriteResponseModelResponses)
def delete_favorite(buyer_id: str, property_id: str):
    """
    Deletes a favorite property for a buyer.
    """
    buyer_db = BuyerDB()
    result = buyer_db.delete_favorite(buyer_id, property_id)
    if result == 400:
        raise HTTPException(status_code=result, detail="Invalid input.")
    elif result == 500:
        raise HTTPException(status_code=result, detail="Failed to delete favorite.")
    elif result == 200:
        return JSONResponse(status_code=result, content={"detail": "Favorite deleted successfully."})

@buyer_router.put("/{buyer_id}/favorites/{property_id}", response_model=ResponseModels.SuccessModel, responses=ResponseModels.UpdateFavoriteResponseModelResponses)
def update_favorite(buyer_id: str, property_id: str, favorite: FavouriteProperty):
    """
    Updates a favorite property for a buyer.
    """
    buyer_db = BuyerDB()
    result = buyer_db.update_favorite(buyer_id, property_id, favorite.dict())
    if result == 400:
        raise HTTPException(status_code=result, detail="Invalid input.")
    elif result == 500:
        raise HTTPException(status_code=result, detail="Failed to update favorite.")
    elif result == 200:
        return JSONResponse(status_code=result, content={"detail": "Favorite updated successfully."})


# ReservationsBuyer

@buyer_router.post(
    "/reservations",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.CreateReservationBuyerResponseModelResponses
)
def create_reservation_buyer(reservations_buyer_info: CreateReservationBuyer, access_token: str = Depends(JWTHandler())):
    #Check if the buyer_id in the token is the same as the buyer_id in the request
    buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)    
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
    except Exception as e:
        logger.error(f"Error creating buyer reservation: {e}")
        raise HTTPException(status_code=500, detail="Error creating buyer reservation")
    
    if status == 409:
        raise HTTPException(status_code=409, detail="Reservation already exists.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to create reservation.")
    
    return JSONResponse(status_code=201, content={"detail": "Buyer reservation created successfully."})

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
def update_reservations_buyer(reservations_buyer_info: UpdateReservationBuyer):
    reservations_buyer = ReservationsBuyer(
        buyer_id=reservations_buyer_info.buyer_id,
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
    except Exception as e:
        logger.error(f"Error updating buyer reservations: {e}")
        raise HTTPException(status_code=500, detail="Error updating buyer reservations")

    if status == 404:
        raise HTTPException(status_code=404, detail="Reservation not found.")
    if status == 400:
        raise HTTPException(status_code=400, detail="Invalid input data.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to update reservation.")
    
    return reservations_buyer_db.reservations_buyer

@buyer_router.delete(
    "/reservations/{buyer_id}",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.DeleteReservationsBuyerResponseModelResponses
)
def delete_reservations_buyer(buyer_id: str):
    reservations_buyer = ReservationsBuyer(buyer_id=buyer_id, reservations=[])
    reservations_buyer_db = ReservationsBuyerDB(reservations_buyer)
    try:
        status = reservations_buyer_db.delete_reservations_buyer()
    except Exception as e:
        logger.error(f"Error deleting buyer reservations: {e}")
        raise HTTPException(status_code=500, detail="Error deleting buyer reservations")

    if status == 404:
        raise HTTPException(status_code=404, detail="No reservations found or delete failed.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to delete reservation.")
    
    return JSONResponse(status_code=200, content={"detail": "Buyer reservations deleted successfully."})

@buyer_router.delete(
    "/reservations/{buyer_id}/{property_on_sale_id}",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.DeleteReservationsBuyerResponseModelResponses
)
def delete_reservation_buyer(buyer_id: str, property_on_sale_id: str):
    reservations_buyer = ReservationsBuyer(buyer_id=buyer_id, reservations=[])
    reservations_buyer_db = ReservationsBuyerDB(reservations_buyer)
    try:
        status = reservations_buyer_db.delete_reservation_by_property_on_sale_id(property_on_sale_id)
    except Exception as e:
        logger.error(f"Error deleting buyer reservation: {e}")
        raise HTTPException(status_code=500, detail="Error deleting buyer reservation")

    if status == 404:
        raise HTTPException(status_code=404, detail="Reservation not found or delete failed.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to delete reservation.")
    
    return JSONResponse(status_code=200, content={"detail": "Buyer reservation deleted successfully."})


# Analytics


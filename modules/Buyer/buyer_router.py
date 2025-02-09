from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
import json
from entities.MongoDB.Buyer.buyer import Buyer, FavouriteProperty
from bson import ObjectId
from entities.MongoDB.Buyer.db_buyer import BuyerDB
from modules.Buyer.models import response_models as ResponseModels
from modules.Buyer.models.buyer_models import UpdateBuyer
from entities.Redis.ReservationsBuyer.db_reservations_buyer import ReservationsBuyerDB
from entities.Redis.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB
from entities.Redis.ReservationsSeller.db_reservations_seller import ReservationsSellerDB
from entities.Redis.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS, next_weekday
from modules.Buyer.models.buyer_models import CreateReservationBuyer, UpdateReservationBuyer

from modules.Auth.helpers.JwtHandler import JWTHandler
from modules.Auth.helpers.auth_helpers import hash_password

buyer_router = APIRouter(prefix="/buyer", tags=["Buyer"])

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
    
    temp_buyer = Buyer(buyer_id=buyer_id)
    buyer_db = BuyerDB(temp_buyer)
    result = buyer_db.get_profile_info()
    if result == 404:
        raise HTTPException(status_code=404, detail="Buyer not found.")
    elif result == 400:
        raise HTTPException(status_code=400, detail="Invalid buyer ID.")
    elif result == 500:
        raise HTTPException(status_code=500, detail="Internal server error.")
    return buyer_db.buyer

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
    
    buyer_old = Buyer(buyer_id=buyer_id)
    buyer_db = BuyerDB(buyer_old)
    
    # check if email already exists on another buyer
    if buyer.email:
        response=buyer_db.get_buyer_by_email(buyer.email)
        if response == 500:
            raise HTTPException(status_code=response, detail="Failed to update buyer.")
        if response == 200 and buyer_db.buyer.buyer_id != buyer_id:
            raise HTTPException(status_code=409, detail="Email already exists on another buyer.")
    
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
    
    temp_buyer = Buyer(buyer_id=buyer_id)
    buyer_db = BuyerDB(temp_buyer)
    result=buyer_db.get_favourites()
    if result == 404:
        raise HTTPException(status_code=404, detail="Favourites not found or buyer not found.")
    if result == 500:
        raise HTTPException(status_code=500, detail="Failed to retrieve favourites.")
    return buyer_db.buyer.favourites

@buyer_router.post("/favourite", response_model=ResponseModels.SuccessModel, responses=ResponseModels.AddFavouriteResponseModelResponses)
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

@buyer_router.delete("/favourite/{property_on_sale_id}", response_model=ResponseModels.SuccessModel, responses=ResponseModels.DeleteFavouriteResponseModelResponses)
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

# ReservationsBuyer


@buyer_router.get(
    "/reservations",
    response_model=List[ReservationB],
    responses=ResponseModels.GetReservationsBuyerResponses
)
def get_reservations(access_token: str = Depends(JWTHandler())):
    """
    Get reservations for a given buyer_id, 
    before showing the buyer the reservations,
    check if some of them are expired and delete them.
    """
    buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
    
    if buyer_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "buyer":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    reservations_buyer = ReservationsBuyer(buyer_id=buyer_id)
    reservations_buyer_db = ReservationsBuyerDB(reservations_buyer)
    status = reservations_buyer_db.update_expired_reservations()
    if status == 500:
        raise HTTPException(status_code=500, detail="Error updating expired reservations")
    if status == 404:
        raise HTTPException(status_code=404, detail="No reservations found for buyer")
    return reservations_buyer_db.reservations_buyer.reservations

@buyer_router.post(
    "/reservation",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.CreateReservationBuyerResponses
)
def create_reservation(book_now_info: CreateReservationBuyer, access_token: str = Depends(JWTHandler())):
    buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
    
    
    if buyer_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "buyer":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    buyer = Buyer(buyer_id=buyer_id)
    buyer_db = BuyerDB(buyer)
    
    status = buyer_db.get_profile_info()
    if status == 404:
        raise HTTPException(status_code=404, detail="Buyer not found")
    if status == 500:
        raise HTTPException(status_code=500, detail="Error decoding buyer data")

    buyer = buyer_db.buyer
    if not all([buyer.name, buyer.surname, buyer.email, buyer.phone_number]):
        raise HTTPException(status_code=500, detail="Incomplete buyer data")

    reservations_buyer = ReservationsBuyer(buyer_id=buyer_id)
    reservations_buyer_db = ReservationsBuyerDB(reservations_buyer)
    reservations_seller = ReservationsSeller(property_on_sale_id=book_now_info.property_on_sale_id)
    reservations_seller_db = ReservationsSellerDB(reservations_seller)

    status = reservations_buyer_db.get_reservations_by_user()
    if status == 500:
        raise HTTPException(status_code=500, detail="Error decoding reservations data")
    if status == 400:
        raise HTTPException(status_code=400, detail="Invalid input data")

    status = reservations_seller_db.get_reservation_seller()
    if status == 500:
        raise HTTPException(status_code=500, detail="Error decoding seller reservations data")
    if status == 400:
        raise HTTPException(status_code=400, detail="Invalid input data")

    new_reservation = ReservationS(
        buyer_id=buyer_id, 
        full_name=f"{buyer.name} {buyer.surname}",
        email=buyer.email,
        phone=buyer.phone_number
    )

    if reservations_seller_db.reservations_seller.reservations is None:
        reservations_seller_db.reservations_seller.reservations = []
    reservations_seller_db.reservations_seller.reservations.append(new_reservation)

    status = reservations_seller_db.create_reservation_seller(
                book_now_info.day,
                book_now_info.time,
                buyer_id,
                book_now_info.max_attendees
            )
    if status == 500:
        raise HTTPException(status_code=500, detail="Error creating seller reservation")
    if status == 409:
        raise HTTPException(status_code=409, detail="Reservation already exists")

    date = next_weekday(book_now_info.day)

    reservations_buyer_db.reservations_buyer.reservations = [
        ReservationB(
            property_on_sale_id = book_now_info.property_on_sale_id, 
            date = date, 
            time = book_now_info.time, 
            thumbnail = book_now_info.thumbnail, 
            address = book_now_info.address
        )
    ]
    status = reservations_buyer_db.create_reservation_buyer()
    
    # if error occurs, rollback the reservation
    if status != 201:
        reservations_seller_db.delete_reservation_seller_by_buyer_id(buyer_id)
        return JSONResponse(status_code=500, content={"detail": "Error creating reservation"})

    return JSONResponse(status_code=201, content={"detail": "Reservation created successfully"})

@buyer_router.delete(
    "/reservation/{property_on_sale_id}",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.DeleteReservationsBuyerResponses
)
def delete_reservation_by_buyer_and_property(property_on_sale_id: str, access_token: str = Depends(JWTHandler())):
    """
    Delete a buyer reservation for a given buyer_id and 
    property_on_sale_id and remove the seller reservation.
    """
    if not ObjectId.is_valid(property_on_sale_id):
        raise HTTPException(status_code=400, detail="Invalid property_on_sale_id")
    
    buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if buyer_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "buyer":
        raise HTTPException(status_code=401, detail="Invalid access token")

    reservations_buyer = ReservationsBuyer(buyer_id=buyer_id)
    reservations_buyer_db = ReservationsBuyerDB(reservations_buyer)
    reservations_seller = ReservationsSeller(property_on_sale_id=property_on_sale_id)
    reservations_seller_db = ReservationsSellerDB(reservations_seller)

    status = reservations_buyer_db.get_reservations_by_user()
    if status == 500:
        raise HTTPException(status_code=500, detail="Error decoding buyer reservations data")
    if status == 404:
        raise HTTPException(status_code=404, detail="No reservations found for buyer")

    status = reservations_seller_db.get_reservation_seller()
    if status == 500:
        raise HTTPException(status_code=500, detail="Error decoding seller reservations data")
    if status == 404:
        raise HTTPException(status_code=404, detail="No reservations found for seller")

    # Check if the buyer has a reservation for the given property
    buyer_reservations = reservations_buyer_db.reservations_buyer.reservations
    if not buyer_reservations:
        raise HTTPException(status_code=404, detail="No reservations found for buyer")
    buyer_reservations = [res for res in buyer_reservations if res.property_on_sale_id == property_on_sale_id]
    if not buyer_reservations:
        raise HTTPException(status_code=404, detail="No reservations found for buyer")
    
    # Check if the seller has a reservation for the given buyer
    seller_reservations = reservations_seller_db.reservations_seller.reservations
    if not seller_reservations:
        raise HTTPException(status_code=404, detail="No reservations found for seller")
    seller_reservations = [res for res in seller_reservations if res.buyer_id == buyer_id]
    if not seller_reservations:
        raise HTTPException(status_code=404, detail="No reservations found for seller")
    
    # Delete the buyer reservation
    status = reservations_buyer_db.delete_reservation_by_property_on_sale_id(property_on_sale_id)
    if status == 500:
        raise HTTPException(status_code=500, detail="Error deleting buyer reservation")
    if status == 404:
        raise HTTPException(status_code=404, detail="No reservations found for buyer")
    
    # Delete the seller reservation
    status = reservations_seller_db.delete_reservation_seller_by_buyer_id(buyer_id)
    
    # if error occurs, rollback the reservation
    if status != 200:
        reservations_buyer_db.create_reservation_buyer()
        return JSONResponse(status_code=500, content={"detail": "Error deleting reservation"})

    
    return JSONResponse(status_code=200, content={"detail": "Reservation deleted successfully"})




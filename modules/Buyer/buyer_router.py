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

@buyer_router.get("/profile_info", response_model=ResponseModels.BuyerInfoResponseModel, responses=ResponseModels.GetBuyerResponseModelResponses)
def get_buyer(access_token: str = Depends(JWTHandler())):
    """
    Retrieve the buyer's profile info.

    Authorization:
        access_token (str): The JWT access token for authentication.

    Raises:
        HTTPException: 401 if the token is invalid or the user is not a buyer.
                       404 if the buyer is not found.
                       400 if the buyer ID is invalid.
                       500 if there is an internal server error.

    Returns:
        Buyer: The buyer's data.
    """
    buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if buyer_id is None or user_type != "buyer":
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
    Update an existing buyer.

    Authorization:
        access_token (str): The JWT access token for authentication.
    
    Body: (UpdateBuyer): The new buyer data to update.

    Raises:
        HTTPException: 401 if the token is invalid or the user is not a buyer.
                       409 if the email already exists.
                       400 if the buyer ID is missing.
                       404 if the buyer is not found.
                       500 if there is an error updating the buyer.

    Returns:
        JSONResponse: A success message if the update is successful.
    """
    buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if buyer_id is None or user_type != "buyer":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    buyer_old = Buyer(buyer_id=buyer_id)
    buyer_db = BuyerDB(buyer_old)
    
    # Check if email already exists on another buyer
    if buyer.email:
        response=buyer_db.get_buyer_by_email(buyer.email)
        if response == 500:
            raise HTTPException(status_code=response, detail="Failed to update buyer.")
        if response == 200 and buyer_db.buyer.buyer_id != buyer_id:
            raise HTTPException(status_code=409, detail="Email already exists on another buyer.")
    
    # Check if there's a password to crypt
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
    
@buyer_router.delete("/", response_model=ResponseModels.SuccessModel, responses=ResponseModels.DeleteBuyerResponseModelResponses)
def delete_buyer(access_token: str = Depends(JWTHandler())):
    """
    Delete an existing buyer.

    Authorization:
        access_token (str): The JWT access token for authentication.

    Raises:
        HTTPException: 401 if the token is invalid or the user is not a buyer.
                       404 if the buyer is not found.
                       500 if there is an error deleting the buyer.

    Returns:
        JSONResponse: A success message if the deletion is successful.
    """
    buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if buyer_id is None or user_type != "buyer":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    buyer = Buyer(buyer_id=buyer_id)
    buyer_db = BuyerDB(buyer)
    result = buyer_db.delete_buyer_by_id(buyer_id)
    if result == 404:
        raise HTTPException(status_code=result, detail="Buyer not found.")
    elif result == 500:
        raise HTTPException(status_code=result, detail="Failed to delete buyer.")
    
    reservation_buyer = ReservationsBuyer(buyer_id=buyer_id)
    reservation_buyer_db = ReservationsBuyerDB(reservation_buyer)

    reservation_buyer_db.delete_reservations_buyer()
    if result == 500:
        raise HTTPException(status_code=result, detail="Failed to delete buyer reservations.")
    if result == 404:
        raise HTTPException(status_code=result, detail="No reservations found for buyer.")
    
    # Reservations seller are not deleted, we still give the buyer the possibility to participate in the OpenHouseEvent
    return JSONResponse(status_code=result, content={"detail": "Buyer deleted successfully."})


# Favourites

@buyer_router.get("/favourites", response_model=List[FavouriteProperty], responses=ResponseModels.GetFavouritesResponseModelResponses)
def get_favourites(access_token: str = Depends(JWTHandler())):
    """
    Retrieve the list of a buyer's favourite properties.

    Authorization:
        access_token (str): The JWT access token for authentication.

    Raises:
        HTTPException: 401 if the token is invalid or the user is not a buyer.
                       404 if no favourites are found or the buyer does not exist.
                       500 if there is an error retrieving favourites.

    Returns:
        List[FavouriteProperty]: The list of favourite properties.
    """
    buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if buyer_id is None or user_type != "buyer":
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
    Add a favourite property for a buyer.

    Body:
        (FavouriteProperty): The property to add.
    
    Authorization:
        access_token (str): The JWT access token for authentication.

    Raises:
        HTTPException: 401 if the token is invalid or the user is not a buyer.
                       400 if the input is invalid.
                       500 if there is an error adding the favourite.

    Returns:
        JSONResponse: A success message if the favourite is added.
    """
    buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if buyer_id is None or user_type != "buyer":
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
    Delete a favourite property from a buyer's list.

    Args:
        property_on_sale_id (str): The ID of the property to remove.
    
    Authorization:
        access_token (str): The JWT access token for authentication.

    Raises:
        HTTPException: 400 if the property_on_sale_id is invalid.
                       401 if the token is invalid or the user is not a buyer.
                       500 if there is an error deleting the favourite.

    Returns:
        JSONResponse: A success message if the favourite is deleted.
    """
    if not ObjectId.is_valid(property_on_sale_id):
        raise HTTPException(status_code=400, detail="Invalid input.")
    buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if buyer_id is None or user_type != "buyer":
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
    Retrieve and update expired reservations for a buyer.

    Authorization:
        access_token (str): The JWT access token for authentication.

    Raises:
        HTTPException: 401 if the token is invalid or the user is not a buyer.
                       500 if there is an error updating reservations.
                       404 if no reservations are found.

    Returns:
        List[ReservationB]: The list of the buyer's reservations.
    """
    buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
    
    if buyer_id is None or user_type != "buyer":
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
    """
    Create a new reservation updating the buyer's reservations list and the seller's reservations list. It checks if the buyer already has a reservation for the same property and if number of attendees is not exceeded.

    Authorization:
        access_token (str): The JWT access token for authentication.
    
    Body:
        (CreateReservationBuyer): The data necessary to create.

    Raises:
        HTTPException: 401 if the token is invalid or the user is not a buyer.
                       404 if the buyer is not found.
                       500 if there is an error decoding buyer data.
                       400 if the input data is invalid.
                       409 if there is a conflict in reservation.
                       500 if there is an error creating the reservation.

    Returns:
        JSONResponse: A success message if the reservation is created.
    """
    buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if buyer_id is None or user_type != "buyer":
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
    
    status = reservations_buyer_db.get_reservations_by_user()
    if status == 500:
        raise HTTPException(status_code=500, detail="Error decoding reservations data")
    if status == 400:
        raise HTTPException(status_code=400, detail="Invalid input data")
    #check if the buyer already has a reservation for the same property
    if reservations_buyer_db.reservations_buyer.reservations:
        for res in reservations_buyer_db.reservations_buyer.reservations:
            if res.property_on_sale_id == book_now_info.property_on_sale_id:
                raise HTTPException(status_code=409, detail="Reservation already exists")
            
    reservations_seller = ReservationsSeller(property_on_sale_id=book_now_info.property_on_sale_id)
    reservations_seller_db = ReservationsSellerDB(reservations_seller)

    new_reservation = ReservationS(
        buyer_id=buyer_id, 
        full_name=f"{buyer.name} {buyer.surname}",
        email=buyer.email,
        phone=buyer.phone_number
    )

    status = reservations_seller_db.handle_book_now_transaction(new_reservation, book_now_info.day, book_now_info.time, buyer_id, book_now_info.max_attendees)
    if status == 400:
        raise HTTPException(status_code=400, detail="Invalid input data")
    if status == 500:
        raise HTTPException(status_code=500, detail="Error creating reservation")
    
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
    
    # If error occurs, rollback the reservation
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
    Delete a reservation for a given buyer and property, updating the buyer's reservations list and the seller's reservations list ensuring data consistency.

    Args:
        property_on_sale_id (str): The ID of the property for which to delete the reservation.
    
    Authorization:
        access_token (str): The JWT access token for authentication.

    Raises:
        HTTPException: 400 if the property_on_sale_id is invalid.
                       401 if the token is invalid or the user is not a buyer.
                       500 or 404 depending on the reservation lookup failure.
                       500 if there is an error deleting the reservation.

    Returns:
        JSONResponse: A success message if the reservation is deleted.
    """
    if not ObjectId.is_valid(property_on_sale_id):
        raise HTTPException(status_code=400, detail="Invalid property_on_sale_id")
    
    buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if buyer_id is None or user_type != "buyer":
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
    
    # If error occurs, rollback the reservation
    if status != 200:
        reservations_buyer_db.create_reservation_buyer()
        return JSONResponse(status_code=500, content={"detail": "Error deleting reservation"})

    
    return JSONResponse(status_code=200, content={"detail": "Reservation deleted successfully"})




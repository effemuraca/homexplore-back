from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import logging
import json
from entities.Redis.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB
from entities.Redis.ReservationsBuyer.db_reservations_buyer import ReservationsBuyerDB
from modules.ReservationsBuyer.models import response_models as ResponseModels
from modules.ReservationsBuyer.models.reservations_buyer_models import CreateReservationBuyer, UpdateReservationBuyer

reservations_buyer_router = APIRouter(prefix="/reservations_buyer", tags=["reservations_buyer"])

# Configura il logger
logger = logging.getLogger(__name__)

@reservations_buyer_router.post(
    "/create_reservation_buyer",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.CreateReservationBuyerResponseModelResponses
)
def create_reservation_buyer(reservations_buyer_info: CreateReservationBuyer):
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
        status = reservations_buyer_db.create_reservation_buyer()
    except Exception as e:
        logger.error(f"Error creating buyer reservation: {e}")
        raise HTTPException(status_code=500, detail="Error creating buyer reservation")
    
    if status == 409:
        raise HTTPException(status_code=409, detail="Reservation already exists.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to create reservation.")
    
    return JSONResponse(status_code=201, content={"detail": "Buyer reservation created successfully."})

@reservations_buyer_router.get(
    "/get_reservations_buyer/{buyer_id}",
    response_model=ReservationsBuyer,
    responses=ResponseModels.GetReservationsBuyerResponseModelResponses
)
def get_reservations_buyer(buyer_id: str):
    reservations_buyer = ReservationsBuyer(buyer_id=buyer_id, reservations=[])
    reservations_buyer_db = ReservationsBuyerDB(reservations_buyer)
    try:
        status = reservations_buyer_db.get_reservations_by_user()

    except Exception as e:
        logger.error(f"Error retrieving buyer reservations: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving buyer reservations")
    
    if status == 404:
        raise HTTPException(status_code=404, detail="No reservations found for buyer.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to retrieve reservations.")
    
    return reservations_buyer_db.reservations_buyer

@reservations_buyer_router.put(
    "/update_reservations_buyer",
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

@reservations_buyer_router.delete(
    "/delete_reservations_buyer/{buyer_id}",
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

@reservations_buyer_router.delete(
    "/delete_reservation_buyer/{buyer_id}/{property_on_sale_id}",
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
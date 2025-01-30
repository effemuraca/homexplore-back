from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import logging
from entities.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS
from entities.ReservationsSeller.db_reservations_seller import ReservationsSellerDB
from modules.ReservationsSeller.models import response_models as ResponseModels
from modules.ReservationsSeller.models.reservations_seller_models import CreateReservationSeller, UpdateReservationSeller

reservations_seller_router = APIRouter(prefix="/reservations_seller", tags=["reservations_seller"])

# Configure the logger
logger = logging.getLogger(__name__)

@reservations_seller_router.post("/reservations_seller", response_model=ResponseModels.SuccessModel, responses=ResponseModels.CreateReservationSellerResponseModelResponses)
def create_reservation_seller(reservations_seller_info: CreateReservationSeller):
    reservations_seller = ReservationsSeller(
        property_id=reservations_seller_info.property_id,
        reservations=[ReservationS(buyer_id=reservations_seller_info.buyer_id, full_name=reservations_seller_info.full_name, email=reservations_seller_info.email, phone=reservations_seller_info.phone)]
    )
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    try:
        status = reservations_seller_db.create_reservation_seller(reservations_seller_info.seconds)
    except Exception as e:
        logger.error(f"Error creating seller reservation: {e}")
        raise HTTPException(status_code=500, detail="Error creating seller reservation")
    if status == 409:
        raise HTTPException(status_code=409, detail="Reservation already exists")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to create reservation.")
    return JSONResponse(status_code=201, content={"detail": "Seller reservation created"})

@reservations_seller_router.get("/reservations_seller", response_model=ReservationsSeller, responses=ResponseModels.GetReservationsSellerResponseModelResponses)
def get_reservations_seller(property_id: str):
    reservations_seller = ReservationsSeller(property_id=property_id)
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    try:
        status = reservations_seller_db.get_reservations_seller_by_property_id()
    except Exception as e:
        logger.error(f"Error retrieving seller reservations: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving seller reservations")

    if status == 404:
        raise HTTPException(status_code=404, detail="No reservations found.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to retrieve reservations.")
    return reservations_seller_db.reservations_seller

@reservations_seller_router.put("/reservations_seller", response_model=ReservationsSeller, responses=ResponseModels.UpdateReservationsSellerResponseModelResponses)
def update_reservations_seller(reservations_seller_info: UpdateReservationSeller):
    reservations_seller = ReservationsSeller(
        property_id=reservations_seller_info.property_id,
        reservations=[ReservationS(buyer_id=reservations_seller_info.buyer_id, full_name=reservations_seller_info.full_name, email=reservations_seller_info.email, phone=reservations_seller_info.phone)]
    )
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    try:
        status = reservations_seller_db.update_reservation_seller()
    except Exception as e:
        logger.error(f"Error updating seller reservations: {e}")
        raise HTTPException(status_code=500, detail="Error updating seller reservations")

    if status == 404:
        raise HTTPException(status_code=404, detail="Reservation not found.")
    if status == 400:
        raise HTTPException(status_code=400, detail="Invalid input data.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to update reservation.")
    return reservations_seller_db.reservations_seller

@reservations_seller_router.delete("/reservations_seller", response_model=ResponseModels.SuccessModel, responses=ResponseModels.DeleteReservationsSellerResponseModelResponses)
def delete_reservations_seller(property_id: str):
    reservations_seller = ReservationsSeller(property_id=property_id)
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    try:
        status = reservations_seller_db.delete_reservations_seller()
    except Exception as e:
        logger.error(f"Error deleting seller reservations: {e}")
        raise HTTPException(status_code=500, detail="Error deleting seller reservations")

    if status == 404:
        raise HTTPException(status_code=404, detail="Reservation not found or delete failed.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to delete reservation.")
    return JSONResponse(status_code=200, content={"detail": "Reservations deleted successfully."})

@reservations_seller_router.delete("/reservations_seller/{buyer_id}/{property_id}", response_model=ResponseModels.SuccessModel, responses=ResponseModels.DeleteReservationsSellerResponseModelResponses)
def delete_reservation_seller_by_buyer_id(buyer_id: str, property_id: str):
    reservations_seller = ReservationsSeller(property_id=property_id, reservations=[ReservationS(buyer_id=buyer_id)])
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    try:
        status = reservations_seller_db.delete_reservation_seller_by_property_id_and_buyer_id(buyer_id)
    except Exception as e:
        logger.error(f"Error deleting seller reservation: {e}")
        raise HTTPException(status_code=500, detail="Error deleting seller reservation")

    if status == 404:
        raise HTTPException(status_code=404, detail="Reservation not found or delete failed.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to delete reservation.")
    return JSONResponse(status_code=200, content={"detail": "Seller reservation deleted successfully."})
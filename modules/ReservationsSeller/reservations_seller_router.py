import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from entities.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS
from entities.ReservationsSeller.db_reservations_seller import ReservationsSellerDB
from modules.ReservationsSeller.models import response_models as ResponseModels
from modules.ReservationsSeller.models.reservations_seller_models import CreateReservationSeller, UpdateReservationSeller

logger = logging.getLogger(__name__)
reservations_seller_router = APIRouter(prefix="/reservations_seller", tags=["reservations_seller"])

@reservations_seller_router.post(
    "/",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.CreateReservationSellerResponseModelResponses
)
def create_reservation_seller(reservations_seller_info: CreateReservationSeller):
    reservations_seller = ReservationsSeller(
        property_id=reservations_seller_info.property_id,
        reservations=[ReservationS(
            buyer_id=reservations_seller_info.buyer_id,
            full_name=reservations_seller_info.full_name,
            email=reservations_seller_info.email,
            phone=reservations_seller_info.phone
        )],
        area=reservations_seller_info.area
    )
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    try:
        status = reservations_seller_db.create_reservation_seller(
            reservations_seller_info.day,
            reservations_seller_info.time
        )
    except Exception as e:
        logger.error(f"Error creating seller reservation: {e}")
        raise HTTPException(status_code=500, detail="Error creating seller reservation")
    if status == 409:
        raise HTTPException(status_code=409, detail="Reservation already exists")
    if status == 400:
        raise HTTPException(status_code=400, detail="Invalid input or missing reservation info.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to create reservation.")
    return JSONResponse(status_code=201, content={"detail": "Seller reservation created"})

@reservations_seller_router.get(
    "/",
    response_model=ReservationsSeller,
    responses=ResponseModels.GetReservationsSellerResponseModelResponses
)
def get_reservations_seller(property_id: str):
    reservations_seller = ReservationsSeller(property_id=property_id)
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    try:
        status = reservations_seller_db.get_reservation_seller()
    except Exception as e:
        logger.error(f"Error retrieving seller reservations: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving seller reservations")
    if status == 404:
        raise HTTPException(status_code=404, detail="No reservations found.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to retrieve reservations.")
    return reservations_seller_db.reservations_seller

@reservations_seller_router.put(
    "/",
    response_model=ReservationsSeller,
    responses=ResponseModels.UpdateReservationsSellerResponseModelResponses
)
def update_reservations_seller(reservations_seller_info: UpdateReservationSeller):
    if not reservations_seller_info.buyer_id:
        raise HTTPException(status_code=400, detail="Missing buyer_id for update.")
    
    reservations_seller = ReservationsSeller(
        property_id=reservations_seller_info.property_id,
        reservations=[ReservationS(
            buyer_id=reservations_seller_info.buyer_id,
            full_name=reservations_seller_info.full_name,
            email=reservations_seller_info.email,
            phone=reservations_seller_info.phone
        )]
    )
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    try:
        updated_data = {
            "full_name": reservations_seller_info.full_name,
            "email": reservations_seller_info.email,
            "phone": reservations_seller_info.phone
        }
        status = reservations_seller_db.update_reservation_seller(
            reservations_seller_info.buyer_id, updated_data
        )
    except HTTPException as he:
        raise he
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

@reservations_seller_router.put(
    "/bulk",
    response_model=ReservationsSeller,
    responses=ResponseModels.UpdateReservationsSellerResponseModelResponses
)
def update_entire_reservations_seller(reservations_seller_info: ReservationsSeller):
    reservations_seller_db = ReservationsSellerDB(reservations_seller_info)
    try:
        status = reservations_seller_db.update_entire_reservation_seller(area=reservations_seller_info.area)
    except Exception as e:
        logger.error(f"Error updating entire seller reservations: {e}")
        raise HTTPException(status_code=500, detail="Error updating entire seller reservations")
    if status == 400:
        raise HTTPException(status_code=400, detail="Maximum reservations exceeded.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to update entire reservations.")
    return reservations_seller_db.reservations_seller

@reservations_seller_router.delete(
    "/",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.DeleteReservationsSellerResponseModelResponses
)
def delete_reservations_seller(property_id: str):
    reservations_seller = ReservationsSeller(property_id=property_id)
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    try:
        status = reservations_seller_db.delete_entire_reservation_seller()
    except Exception as e:
        logger.error(f"Error deleting seller reservations: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete reservation.")
    if status == 404:
        raise HTTPException(status_code=404, detail="Reservation not found or delete failed.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to delete reservation.")
    return JSONResponse(status_code=200, content={"detail": "Reservations deleted successfully."})

@reservations_seller_router.delete(
    "/{buyer_id}/{property_id}",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.DeleteReservationsSellerResponseModelResponses
)
def delete_reservation_seller_by_buyer_id(buyer_id: str, property_id: str):
    reservations_seller = ReservationsSeller(
        property_id=property_id,
        reservations=[ReservationS(buyer_id=buyer_id)]
    )
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    try:
        status = reservations_seller_db.delete_reservation_seller_by_buyer_id(buyer_id)
    except Exception as e:
        logger.error(f"Error deleting reservation for buyer_id={buyer_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete reservation.")
    if status == 404:
        raise HTTPException(status_code=404, detail="Reservation not found or delete failed.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to delete reservation.")
    return JSONResponse(status_code=200, content={"detail": "Seller reservation deleted successfully."})
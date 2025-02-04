import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from entities.Redis.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS
from entities.Redis.ReservationsSeller.db_reservations_seller import ReservationsSellerDB
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
        property_on_sale_id=reservations_seller_info.property_on_sale_id,
        reservations=[ReservationS(
            buyer_id=reservations_seller_info.buyer_id,
            full_name=reservations_seller_info.full_name,
            email=reservations_seller_info.email,
            phone=reservations_seller_info.phone
        )]
    )
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    status = reservations_seller_db.create_reservation_seller(
        day=reservations_seller_info.day,
        time=reservations_seller_info.time,
        buyer_id=reservations_seller_info.buyer_id,
        max_reservations=reservations_seller_info.max_reservations
    )
    if status == 409:
        raise HTTPException(status_code=409, detail="Reservation already exists.")
    if status == 400:
        raise HTTPException(status_code=400, detail="Invalid input provided.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to create reservation.")
    return JSONResponse(status_code=201, content={"detail": "Seller reservation created successfully."})
   
@reservations_seller_router.get(
    "/",
    response_model=ReservationsSeller,
    responses=ResponseModels.GetReservationsSellerResponseModelResponses
)
def get_reservations_seller(property_on_sale_id: str):
    reservations_seller = ReservationsSeller(property_on_sale_id=property_on_sale_id)
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    status = reservations_seller_db.get_reservation_seller()
    if status == 404:
        raise HTTPException(status_code=404, detail="No reservations found.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to fetch reservations.")
    return reservations_seller_db.reservations_seller

@reservations_seller_router.put(
    "/",
    response_model=ReservationsSeller,
    responses=ResponseModels.UpdateReservationsSellerResponseModelResponses
)
def update_reservations_seller(reservations_seller_info: UpdateReservationSeller):
    if not reservations_seller_info.buyer_id:
        raise HTTPException(status_code=400, detail="Buyer ID is required for update.")
    reservations_seller = ReservationsSeller(
        property_on_sale_id=reservations_seller_info.property_on_sale_id,
        reservations=[ReservationS(
            buyer_id=reservations_seller_info.buyer_id,
            full_name=reservations_seller_info.full_name,
            email=reservations_seller_info.email,
            phone=reservations_seller_info.phone
        )]
    )
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    status = reservations_seller_db.update_reservation_seller(reservations_seller_info.buyer_id, reservations_seller_info.dict(exclude_unset=True, exclude={"property_on_sale_id"}))
    if status == 404:
        raise HTTPException(status_code=404, detail="Reservation not found.")
    if status == 400:
        raise HTTPException(status_code=400, detail="Invalid input provided.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to update reservation.")
    reservations_seller_db.get_reservation_seller()
    return reservations_seller_db.reservations_seller

@reservations_seller_router.delete(
    "/",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.DeleteReservationsSellerResponseModelResponses
)
def delete_reservations_seller(property_on_sale_id: str):
    reservations_seller = ReservationsSeller(property_on_sale_id=property_on_sale_id)
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    status = reservations_seller_db.delete_entire_reservation_seller()
    if status == 404:
        raise HTTPException(status_code=404, detail="Reservation not found or delete failed.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to delete reservation.")
    
@reservations_seller_router.delete(
    "/{buyer_id}/{property_on_sale_id}",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.DeleteReservationsSellerResponseModelResponses
)
def delete_reservation_seller_by_buyer_id(buyer_id: str, property_on_sale_id: str):
    reservations_seller = ReservationsSeller(
        property_on_sale_id=property_on_sale_id,
        reservations=[ReservationS(buyer_id=buyer_id)]
    )
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    status = reservations_seller_db.delete_reservation_seller_by_buyer_id(buyer_id)
    if status == 404:
        raise HTTPException(status_code=404, detail="Reservation not found.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to delete reservation.")
    return JSONResponse(status_code=200, content={"detail": "Seller reservation deleted successfully."})

@reservations_seller_router.put(
    "/date_and_time",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.UpdateReservationsSellerResponseModelResponses
)
def update_reservations_seller_date_and_time(property_on_sale_id: str, day: str, time: str):
    reservations_seller = ReservationsSeller(
        property_on_sale_id=property_on_sale_id,
        reservations=[]
    )
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    status = reservations_seller_db.update_day_and_time(day, time)
    if status == 404:
        raise HTTPException(status_code=404, detail="Reservation not found.")
    if status == 400:
        raise HTTPException(status_code=400, detail="Invalid input provided.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to update reservation.")
    return JSONResponse(status_code=200, content={"detail": "Seller reservation updated successfully."})
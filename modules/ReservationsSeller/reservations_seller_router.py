from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from entities.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS
from entities.ReservationsSeller.db_reservations_seller import ReservationsSellerDB
from modules.ReservationsSeller.models import response_models as ResponseModels

reservations_seller_router = APIRouter(prefix="/reservations_seller", tags=["reservations_seller"])

# Configure the logger
import logging
logger = logging.getLogger(__name__)

@reservations_seller_router.get(
    "/{property_id}",
    response_model=ReservationsSeller,
    responses=ResponseModels.ReservationsSellerResponseModelResponses
)
def get_reservations_seller(property_id: int):
    """
    Recupera tutte le prenotazioni del seller per un dato property_id.
    """
    db = ReservationsSellerDB(ReservationsSeller(property_id=property_id))
    result = db.get_reservations_seller_by_property_id(property_id)
    if not result:
        raise HTTPException(status_code=404, detail="No reservations found for this property.")
    return result

@reservations_seller_router.post(
    "/",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.CreateReservationsSellerResponseModelResponses
)
def create_reservations_seller(property_id: int, reservation_info: ReservationS):
    """
    Crea una nuova prenotazione per un seller.
    """
    if not property_id or not reservation_info:
        raise HTTPException(status_code=400, detail="Property ID and reservation info are required.")
    
    db = ReservationsSellerDB(ReservationsSeller(property_id=property_id))
    success = db.create_reservation_seller(property_id, reservation_info)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to create reservation.")
    
    return {"detail": "Reservation created successfully."}

@reservations_seller_router.delete(
    "/{property_id}/{user_id}",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.DeleteReservationsSellerResponseModelResponses
)
def delete_reservations_seller(property_id: int, user_id: int):
    """
    Cancella una prenotazione per un seller specifico.
    """
    db = ReservationsSellerDB(ReservationsSeller(property_id=property_id))
    success = db.delete_reservation_seller(property_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reservation not found or delete failed.")
    return {"detail": "Reservation deleted successfully."}

@reservations_seller_router.put(
    "/{property_id}/{user_id}",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.UpdateReservationsSellerResponseModelResponses
)
def update_reservation_seller(property_id: int, user_id: int, reservation_info: ReservationS):
    """
    Aggiorna una prenotazione esistente per un seller.
    """
    if not reservation_info:
        raise HTTPException(status_code=400, detail="Reservation info is required.")
    
    db = ReservationsSellerDB(ReservationsSeller(property_id=property_id))
    success = db.update_reservation_seller(property_id, user_id, reservation_info)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update reservation.")
    
    return {"detail": "Reservation updated successfully."}
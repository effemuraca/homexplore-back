from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from modules.ReservationsSeller.models import response_models as ResponseModels
from modules.ReservationsSeller.models import reservations_seller_models as ReservationsSellerModels
from entities.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS
from entities.ReservationsSeller.db_reservations_seller import ReservationsSellerDB
import logging

reservations_seller_router = APIRouter(prefix="/reservations_seller", tags=["reservations_seller"])

# Configure the logger
logger = logging.getLogger(__name__)

@reservations_seller_router.get(
    "/reservations_seller",
    response_model=ReservationsSeller,
    responses=ResponseModels.ReservationsSellerResponseModelResponses
)
def get_reservations_seller(property_id: int):
    """
    Recupera tutte le prenotazioni del seller per un dato property_id.
    """
    db = ReservationsSellerDB(ReservationsSeller())
    result = db.get_reservations_seller_by_property_id(property_id)
    if not result:
        logger.warning(f"No seller reservations found for property_id={property_id}.")
        raise HTTPException(status_code=404, detail="No reservations found")
    return db.reservations_seller

@reservations_seller_router.post(
    "/reservations_seller",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.CreateReservationsSellerResponseModelResponses
)
def create_reservations_seller(property_id: int, reservation_info: ReservationS):
    """
    Crea una nuova prenotazione per un dato property_id.
    """
    db = ReservationsSellerDB(ReservationsSeller())
    try:
        check = db.create_reservation_seller(property_id, reservation_info)
    except Exception as e:
        logger.error(f"Error creating seller reservation: {e}")
        raise HTTPException(status_code=500, detail="Error creating reservation")
    if not check:
        logger.warning(f"Reservation already exists or failed to create for property_id={property_id}, user_id={reservation_info.user_id}.")
        raise HTTPException(status_code=500, detail="Reservation already exists or failed to create")
    logger.info(f"Reservation created successfully for property_id={property_id}, user_id={reservation_info.user_id}.")
    return JSONResponse(status_code=201, content={"detail": "Reservation created"})

@reservations_seller_router.delete(
    "/reservations_seller",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.DeleteReservationsSellerResponseModelResponses
)
def delete_reservations_seller(property_id: int, user_id: int):
    """
    Elimina una prenotazione specifica per un dato property_id e user_id.
    """
    db = ReservationsSellerDB(ReservationsSeller())
    try:
        check = db.delete_reservations_seller_by_property_id_and_user_id(property_id, user_id)
    except Exception as e:
        logger.error(f"Error deleting seller reservations: {e}")
        raise HTTPException(status_code=500, detail="Error deleting reservations")
    if not check:
        logger.warning(f"Failed to delete reservation for property_id={property_id}, user_id={user_id}.")
        raise HTTPException(status_code=404, detail="Reservation not found")
    logger.info(f"Reservation deleted successfully for property_id={property_id}, user_id={user_id}.")
    return JSONResponse(status_code=200, content={"detail": "Reservations deleted"})

@reservations_seller_router.put(
    "/reservations_seller",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.UpdateReservationsSellerResponseModelResponses
)
def update_reservation_seller(property_id: int, user_id: int, reservation_info: ReservationS):
    """
    Aggiorna una prenotazione esistente per un dato property_id e user_id.
    """
    db = ReservationsSellerDB(ReservationsSeller())
    try:
        check = db.update_reservation_seller(property_id, user_id, reservation_info)
    except Exception as e:
        logger.error(f"Error updating seller reservation: {e}")
        raise HTTPException(status_code=500, detail="Error updating reservation")
    if not check:
        logger.warning(f"Reservation not found or failed to update for property_id={property_id}, user_id={user_id}.")
        raise HTTPException(status_code=404, detail="Reservation not found or failed to update")
    logger.info(f"Reservation updated successfully for property_id={property_id}, user_id={user_id}.")
    return JSONResponse(status_code=200, content={"detail": "Reservation updated"})
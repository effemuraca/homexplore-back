from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from modules.ReservationsBuyer.models import response_models as ResponseModels
from modules.ReservationsBuyer.models import reservations_buyer_models as ReservationsBuyerModels
from entities.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB
from entities.ReservationsBuyer.db_reservations_buyer import ReservationsBuyerDB
import logging

reservations_buyer_router = APIRouter(prefix="/reservations_buyer", tags=["reservations_buyer"])

# Configure the logger
logger = logging.getLogger(__name__)

@reservations_buyer_router.get(
    "/reservations_buyer",
    response_model=ReservationsBuyer,
    responses=ResponseModels.ReservationsBuyerResponseModelResponses
)
def get_reservations_by_user(user_id: int):
    """
    Recupera tutte le prenotazioni del buyer per un dato user_id.
    """
    db = ReservationsBuyerDB(ReservationsBuyer())
    reservations = db.get_reservations_by_user(user_id)
    if reservations is None:
        logger.warning(f"No reservations found for user_id={user_id}.")
        raise HTTPException(status_code=404, detail="No reservations found")
    return db.reservations_buyer

@reservations_buyer_router.post(
    "/reservations_buyer",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.CreateReservationsBuyerResponseModelResponses
)
def create_reservations_buyer(user_id: int, reservation_info: ReservationB):
    """
    Crea una nuova prenotazione per un dato utente.
    """
    db = ReservationsBuyerDB(ReservationsBuyer())
    try:
        check = db.create_reservation_buyer(user_id, reservation_info)
    except Exception as e:
        logger.error(f"Error creating buyer reservation: {e}")
        raise HTTPException(status_code=500, detail="Error creating reservation")
    if not check:
        logger.warning(f"Reservation already exists or failed to create for user_id={user_id}, property_id={reservation_info.property_id}.")
        raise HTTPException(status_code=500, detail="Reservation already exists or failed to create")
    logger.info(f"Reservation created successfully for user_id={user_id}, property_id={reservation_info.property_id}.")
    return ResponseModels.SuccessModel(detail="Reservation created")

@reservations_buyer_router.delete(
    "/reservations_buyer",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.DeleteReservationsBuyerResponseModelResponses
)
def delete_reservations_by_user(user_id: int):
    """
    Elimina tutte le prenotazioni per un dato utente.
    """
    db = ReservationsBuyerDB(ReservationsBuyer())
    try:
        check = db.delete_reservations_by_user(user_id)
    except Exception as e:
        logger.error(f"Error deleting buyer reservations: {e}")
        raise HTTPException(status_code=500, detail="Error deleting reservations")
    if not check:
        logger.warning(f"Failed to delete reservations for user_id={user_id}.")
        raise HTTPException(status_code=500, detail="Error deleting reservations")
    logger.info(f"Reservations deleted successfully for user_id={user_id}.")
    return ResponseModels.SuccessModel(detail="Reservations deleted")

@reservations_buyer_router.put(
    "/reservations_buyer",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.UpdateReservationsBuyerResponseModelResponses
)
def update_reservation_buyer(user_id: int, property_id: int, reservation_info: ReservationB):
    """
    Aggiorna una prenotazione esistente per un dato utente e property_id.
    """
    db = ReservationsBuyerDB(ReservationsBuyer())
    try:
        check = db.update_reservation_buyer(user_id, property_id, reservation_info)
    except Exception as e:
        logger.error(f"Error updating buyer reservation: {e}")
        raise HTTPException(status_code=500, detail="Error updating reservation")
    if not check:
        logger.warning(f"Reservation not found or failed to update for user_id={user_id}, property_id={property_id}.")
        raise HTTPException(status_code=404, detail="Reservation not found or failed to update")
    logger.info(f"Reservation updated successfully for user_id={user_id}, property_id={property_id}.")
    return ResponseModels.SuccessModel(detail="Reservation updated")
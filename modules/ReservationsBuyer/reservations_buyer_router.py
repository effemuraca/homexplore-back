from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from modules.ReservationsBuyer.models import response_models as ResponseModels
from modules.ReservationsBuyer.models import reservations_buyer_models as ReservationsBuyerModels
from entities.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB
from entities.ReservationsBuyer.db_reservations_buyer import ReservationsBuyerDB

reservations_buyer_router = APIRouter(prefix="/reservations_buyer", tags=["reservations_buyer"])

@reservations_buyer_router.get(
    "/reservations_buyer_router",
    response_model=ReservationsBuyer,
    responses=ResponseModels.ReservationsBuyerResponseModelResponses
)
def get_reservations_by_user(user_id: int):
    """
    Retrieve all buyer reservations for a given user_id.
    """
    db = ReservationsBuyerDB(ReservationsBuyer())
    reservations = db.get_reservations_by_user(user_id)
    if reservations is None:
        raise HTTPException(status_code=404, detail="Reservations not found")
    return db.reservations_buyer

@reservations_buyer_router.post(
    "/reservations_buyer_router",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.CreateReservationsBuyerResponseModelResponses
)
def create_reservations_buyer_router(user_id: int, reservation_info: ReservationB):
    """
    Create a new reservation for a given user.
    """
    db = ReservationsBuyerDB(ReservationsBuyer())
    try:
        check = db.create_reservation(user_id, reservation_info)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error creating reservation")
    if not check:
        raise HTTPException(status_code=500, detail="Error creating reservation")
    return JSONResponse(status_code=201, content={"detail": "Reservation created"})

@reservations_buyer_router.delete(
    "/reservations_buyer_router",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.DeleteReservationsBuyerResponseModelResponses
)
def delete_reservations_by_user(user_id: int):
    """
    Delete all reservations for a given user.
    """
    db = ReservationsBuyerDB(ReservationsBuyer())
    check = db.delete_reservations_by_user(user_id)
    if not check:
        raise HTTPException(status_code=500, detail="Error deleting reservations")
    return JSONResponse(status_code=200, content={"detail": "Reservations deleted"})

@reservations_buyer_router.put(
    "/reservations_buyer_router",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.UpdateReservationsBuyerResponseModelResponses
)
def update_reservations_by_user(user_id: int, reservation_info: ReservationB):
    """
    Update an existing reservation for a given user.
    """
    db = ReservationsBuyerDB(ReservationsBuyer())
    try:
        check = db.update_reservation(user_id, reservation_info)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error updating reservation")
    if not check:
        raise HTTPException(status_code=500, detail="Error updating reservation")
    # Rimosso l'ulteriore create per evitare duplicazione
    return JSONResponse(status_code=200, content={"detail": "Reservation updated"})
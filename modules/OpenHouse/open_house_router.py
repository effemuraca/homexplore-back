from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from entities.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB
from entities.ReservationsBuyer.db_reservations_buyer import ReservationsBuyerDB
from modules.OpenHouse.models import response_models as ResponseModels
from modules.OpenHouse.models import open_house_models as OpenHouseModels


open_house_router = APIRouter(prefix="/open_house", tags=["open_house"])

# ReservationsBuyer
#TODO add Depends for authentication with JWT once it's implemented

@open_house_router.get("/reservations_buyer", response_model=ReservationsBuyer, responses=ResponseModels.ReservationsBuyerResponseModelResponses)
def get_reservations_by_user(user_id:int):
    """
    This endpoint retrieves a list of reservations by user id.
    
    @param user_id: the id of the user to retrieve reservations.
    """
    reservations_buyer = ReservationsBuyer(None, None)
    reservations_buyer_db = ReservationsBuyerDB(reservations_buyer)
    reservations_buyer_db.get_reservations_by_user(user_id)
    if reservations_buyer is None:
        raise HTTPException(status_code=404, detail="Reservations not found")
    return reservations_buyer_db.reservations_buyer


@open_house_router.post("/reservations_buyer", response_model=ResponseModels.SuccessModel, responses=ResponseModels.CreateReservationsBuyerResponseModelResponses)
def create_reservations_buyer(user_id:int, reservation_info: ReservationB):
    """
    This endpoint creates a reservation for a user.
    
    @param reservation_info: the information of the reservation to create.
    """
    reservations_buyer = ReservationsBuyer(None, None)
    reservations_buyer_db = ReservationsBuyerDB(reservations_buyer)
    try:
        check = reservations_buyer_db.create_reservation(user_id, reservation_info)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error creating reservation")
    if not check:
        raise HTTPException(status_code=500, detail="Error creating reservation")
    
    return JSONResponse(status_code=201, content={"detail": "Reservation created"})
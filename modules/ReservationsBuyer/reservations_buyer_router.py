from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from modules.ReservationsBuyer.models import response_models as ResponseModels
from modules.ReservationsBuyer.models import reservations_buyer_models as ReservationsBuyerModels
from entities.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB
from entities.ReservationsBuyer.db_reservations_buyer import ReservationsBuyerDB

open_house_router = APIRouter(prefix="/open_house", tags=["open_house"])

#TODO add Depends for authentication with JWT once it's implemented

@open_house_router.get("/reservations_buyer", response_model=ReservationsBuyer, responses=ResponseModels.ReservationsBuyerResponseModelResponses)
def get_reservations_by_user(user_id:int):
    """
    This endpoint retrieves a list of reservations by user id.
    
    @param user_id: the id of the user to retrieve reservations.
    """
    reservations_buyer_db = ReservationsBuyerDB(ReservationsBuyer())
    reservations = reservations_buyer_db.get_reservations_by_user(user_id)
    if reservations is None:
        raise HTTPException(status_code=404, detail="Reservations not found")
    return reservations_buyer_db.reservations_buyer  


@open_house_router.post("/reservations_buyer", response_model=ResponseModels.SuccessModel, responses=ResponseModels.CreateReservationsBuyerResponseModelResponses)
def create_reservations_buyer(user_id:int, reservation_info: ReservationB):
    """
    This endpoint creates a reservation for a user.
    
    @param reservation_info: the information of the reservation to create.
    """
    reservations_buyer_db = ReservationsBuyerDB(ReservationsBuyer())
    try:
        check = reservations_buyer_db.create_reservation(user_id, reservation_info)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error creating reservation")
    if not check:
        raise HTTPException(status_code=500, detail="Error creating reservation")
    
    return JSONResponse(status_code=201, content={"detail": "Reservation created"})

@open_house_router.delete("/reservations_buyer", response_model=ResponseModels.SuccessModel, responses=ResponseModels.DeleteReservationsBuyerResponseModelResponses)
def delete_reservations_by_user(user_id:int):
    """
    This endpoint deletes all reservations for a user.
    
    @param user_id: the id of the user to delete reservations.
    """
    reservations_buyer_db = ReservationsBuyerDB(ReservationsBuyer())
    check = reservations_buyer_db.delete_reservations_by_user(user_id)
    if not check:
        raise HTTPException(status_code=500, detail="Error deleting reservations")
    
    return JSONResponse(status_code=200, content={"detail": "Reservations deleted"})

@open_house_router.put("/reservations_buyer", response_model=ResponseModels.SuccessModel, responses=ResponseModels.UpdateReservationsBuyerResponseModelResponses)
def update_reservations_by_user(user_id:int, reservation_info: ReservationB):
    """
    This endpoint updates a reservation for a user.
    
    @param reservation_info: the information of the reservation to update.
    """
    reservations_buyer_db = ReservationsBuyerDB(ReservationsBuyer())
    check = reservations_buyer_db.update_reservation(user_id, reservation_info)
    if not check:
        raise HTTPException(status_code=500, detail="Error updating reservation")
    check = reservations_buyer_db.create_reservation(user_id, reservation_info)
    if not check:
        raise HTTPException(status_code=500, detail="Error updating reservation")
    
    return JSONResponse(status_code=200, content={"detail": "Reservation updated"})
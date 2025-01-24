from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from entities.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB
from entities.ReservationsBuyer.db_reservations_buyer import ReservationsBuyerDB
from modules.OpenHouse.models import response_models as ResponseModels
from modules.OpenHouse.models import open_house_models as OpenHouseModels
from entities.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS
from entities.ReservationsSeller.db_reservations_seller import ReservationsSellerDB
from entities.OpenHouseEvent.open_house_event import OpenHouseEvent, OpenHouseInfo
from entities.OpenHouseEvent.db_open_house_event import OpenHouseEventDB

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
    reservations = reservations_buyer_db.get_reservations_by_user(user_id)
    if reservations is None:
        raise HTTPException(status_code=404, detail="Reservations not found")
    return reservations  


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

@open_house_router.delete("/reservations_buyer", response_model=ResponseModels.SuccessModel, responses=ResponseModels.DeleteReservationsBuyerResponseModelResponses)
def delete_reservations_by_user(user_id:int):
    """
    This endpoint deletes all reservations for a user.
    
    @param user_id: the id of the user to delete reservations.
    """
    reservations_buyer = ReservationsBuyer(None, None)
    reservations_buyer_db = ReservationsBuyerDB(reservations_buyer)
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
    reservations_buyer = ReservationsBuyer(None, None)
    reservations_buyer_db = ReservationsBuyerDB(reservations_buyer)
    check = reservations_buyer_db.delete_reservations_by_user(user_id)
    if not check:
        raise HTTPException(status_code=500, detail="Error updating reservation")
    check = reservations_buyer_db.create_reservation(user_id, reservation_info)
    if not check:
        raise HTTPException(status_code=500, detail="Error updating reservation")
    
    return JSONResponse(status_code=200, content={"detail": "Reservation updated"})


# ReservationsSeller
@open_house_router.get("/reservations_seller", response_model=ReservationsSeller, responses=ResponseModels.ReservationsSellerResponseModelResponses)
def get_reservations_seller(property_id: int):
    """
    Retrieve reservations for a specific property.
    """
    reservations_seller = ReservationsSellerDB(ReservationsSeller(None, None))
    reservations = reservations_seller.get_reservations_seller_by_property_id(property_id)
    if reservations is None:
        raise HTTPException(status_code=404, detail="Reservations not found")
    return reservations

@open_house_router.post("/reservations_seller", response_model=ResponseModels.SuccessModel, responses=ResponseModels.CreateReservationsSellerResponseModelResponses)
def create_reservations_seller(property_id: int, reservation_info: ReservationS):
    """
    Create a reservation for a property.
    """
    reservations_seller_db = ReservationsSellerDB(ReservationsSeller(None, None))
    try:
        check = reservations_seller_db.create_reservations_seller(property_id, reservation_info)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error creating reservation")
    if not check:
        raise HTTPException(status_code=500, detail="Error creating reservation")
    
    return JSONResponse(status_code=201, content={"detail": "Reservation created"})

@open_house_router.delete("/reservations_seller", response_model=ResponseModels.SuccessModel, responses=ResponseModels.DeleteReservationsSellerResponseModelResponses)
def delete_reservations_seller(property_id: int):
    """
    Delete all reservations for a property.
    """
    reservations_seller_db = ReservationsSellerDB(ReservationsSeller(None, None))
    check = reservations_seller_db.delete_reservations_seller_by_property_id(property_id)
    if not check:
        raise HTTPException(status_code=500, detail="Error deleting reservations")
    
    return JSONResponse(status_code=200, content={"detail": "Reservations deleted"})

@open_house_router.put("/reservations_seller", response_model=ResponseModels.SuccessModel, responses=ResponseModels.UpdateReservationsSellerResponseModelResponses)
def update_reservations_seller(property_id: int, reservation_info: ReservationS):
    """
    Update a reservation for a property.
    """
    reservations_seller_db = ReservationsSellerDB(ReservationsSeller(None, None))
    try:
        check = reservations_seller_db.update_reservations_seller(property_id, reservation_info)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error updating reservation")
    if not check:
        raise HTTPException(status_code=500, detail="Error updating reservation")
    
    return JSONResponse(status_code=200, content={"detail": "Reservation updated"})

# OpenHouseEvent
@open_house_router.get("/open_house_event", response_model=OpenHouseEvent, responses=ResponseModels.OpenHouseEventResponseModelResponses)
def get_open_house_event(property_id: int):
    """
    Retrieve open house event details for a specific property.
    """
    open_house_db = OpenHouseEventDB(OpenHouseEvent(None, None))
    open_house_event = open_house_db.get_open_house_event_by_property(property_id)
    if open_house_event is None:
        raise HTTPException(status_code=404, detail="Open house event not found")
    return open_house_event

@open_house_router.post("/open_house_event", response_model=ResponseModels.SuccessModel, responses=ResponseModels.CreateOpenHouseEventResponseModelResponses)
def create_open_house_event(property_id: int, open_house_info: OpenHouseInfo):
    """
    Create an open house event for a property.
    """
    open_house_db = OpenHouseEventDB(OpenHouseEvent(None, None))
    try:
        success = open_house_db.create_open_house_event(property_id, open_house_info)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error creating open house event")
    if not success:
        raise HTTPException(status_code=500, detail="Error creating open house event")
    
    return JSONResponse(status_code=201, content={"detail": "Open house event created"})

@open_house_router.delete("/open_house_event", response_model=ResponseModels.SuccessModel, responses=ResponseModels.DeleteOpenHouseEventResponseModelResponses)
def delete_open_house_event(property_id: int):
    """
    Delete the open house event for a property.
    """
    open_house_db = OpenHouseEventDB(OpenHouseEvent(None, None))
    success = open_house_db.delete_open_house_event_by_property(property_id)
    if not success:
        raise HTTPException(status_code=500, detail="Error deleting open house event")
    
    return JSONResponse(status_code=200, content={"detail": "Open house event deleted"})

@open_house_router.put("/open_house_event", response_model=ResponseModels.SuccessModel, responses=ResponseModels.UpdateOpenHouseEventResponseModelResponses)
def update_open_house_event(property_id: int, open_house_info: OpenHouseInfo):
    """
    Update the open house event for a property.
    """
    open_house_db = OpenHouseEventDB(OpenHouseEvent(None, None))
    try:
        success = open_house_db.update_open_house_event(property_id, open_house_info)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error updating open house event")
    if not success:
        raise HTTPException(status_code=500, detail="Error updating open house event")
    
    return JSONResponse(status_code=200, content={"detail": "Open house event updated"})

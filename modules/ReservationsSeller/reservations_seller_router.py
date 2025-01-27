from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from modules.ReservationsSeller.models import response_models as ResponseModels
from modules.ReservationsSeller.models import reservations_seller_models as ReservationsSellerModels
from entities.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS
from entities.ReservationsSeller.db_reservations_seller import ReservationsSellerDB

open_house_router = APIRouter(prefix="/open_house", tags=["open_house"])

@open_house_router.get(
    "/reservations_seller",
    response_model=ReservationsSeller,
    responses=ResponseModels.ReservationsSellerResponseModelResponses
)
def get_reservations_seller(property_id: int):
    db = ReservationsSellerDB(ReservationsSeller())
    result = db.get_reservations_seller_by_property_id(property_id)
    if not result:
        raise HTTPException(status_code=404, detail="Reservations not found")
    return db.reservations_seller

@open_house_router.post(
    "/reservations_seller",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.CreateReservationsSellerResponseModelResponses
)
def create_reservations_seller(property_id: int, reservation_info: ReservationS):
    db = ReservationsSellerDB(ReservationsSeller())
    try:
        check = db.create_reservations_seller(property_id, reservation_info)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error creating reservation")
    if not check:
        raise HTTPException(status_code=500, detail="Error creating reservation")
    return JSONResponse(status_code=201, content={"detail": "Reservation created"})

@open_house_router.delete(
    "/reservations_seller",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.DeleteReservationsSellerResponseModelResponses
)
def delete_reservations_seller(property_id: int):
    db = ReservationsSellerDB(ReservationsSeller())
    check = db.delete_reservations_seller_by_property_id(property_id)
    if not check:
        raise HTTPException(status_code=500, detail="Error deleting reservations")
    return JSONResponse(status_code=200, content={"detail": "Reservations deleted"})

@open_house_router.put(
    "/reservations_seller",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.UpdateReservationsSellerResponseModelResponses
)
def update_reservations_seller(property_id: int, reservation_info: ReservationS):
    db = ReservationsSellerDB(ReservationsSeller())
    try:
        check = db.update_reservations_seller(property_id, reservation_info)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error updating reservation")
    if not check:
        raise HTTPException(status_code=500, detail="Error updating reservation")
    return JSONResponse(status_code=200, content={"detail": "Reservation updated"})
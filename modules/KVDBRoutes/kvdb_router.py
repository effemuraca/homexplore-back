from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from modules.ReservationsBuyer.models import response_models as ResponseModels
from modules.KVDBRoutes.models import kvdb_models as KVDBModels
from entities.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB
from entities.ReservationsBuyer.db_reservations_buyer import ReservationsBuyerDB
from entities.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS
from entities.ReservationsSeller.db_reservations_seller import ReservationsSellerDB
from entities.OpenHouseEvent.open_house_event import OpenHouseEvent, OpenHouseInfo
from entities.OpenHouseEvent.db_open_house_event import OpenHouseEventDB


kvdb_router = APIRouter(prefix="/kvdb", tags=["kvdb"])


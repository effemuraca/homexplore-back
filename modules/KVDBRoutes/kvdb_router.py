from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from setup.redis_setup.redis_setup import get_redis_client, WatchError
from modules.KVDBRoutes.models import response_models as ResponseModels
from modules.KVDBRoutes.models import kvdb_models as KVDBModels
from entities.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB
from entities.ReservationsBuyer.db_reservations_buyer import ReservationsBuyerDB
from entities.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS
from entities.ReservationsSeller.db_reservations_seller import ReservationsSellerDB
from entities.OpenHouseEvent.open_house_event import OpenHouseEvent, OpenHouseInfo
from entities.OpenHouseEvent.db_open_house_event import OpenHouseEventDB
import json
import logging

kvdb_router = APIRouter(prefix="/kvdb", tags=["kvdb"])

# Configure the logger
logger = logging.getLogger(__name__)

# Reservation deleted by buyer
@kvdb_router.delete(
    "/reservations_buyer_router",
    response_model=KVDBModels.SuccessModel,
    responses=ResponseModels.DeleteReservationsBuyerResponseModelResponses
)
def delete_reservation_by_user_and_property(user_id: int, property_id: int):
    """
    Delete a buyer reservation for a given user_id and property_id,
    decrement the open house attendees, and remove the seller reservation.
    This is done atomically using Redis transactions (WATCH/MULTI/EXEC).
    """
    buyer_key = f"buyer_id:{user_id}:reservations"
    oh_key = f"property_id:{property_id}:open_house_info"
    seller_key = f"property_id:{property_id}:reservations_seller"
    redis = get_redis_client()

    with redis.pipeline() as pipe:
        while True:
            try:
                pipe.watch(buyer_key, oh_key, seller_key)

                buyer_data = pipe.get(buyer_key)
                oh_data = pipe.get(oh_key)
                seller_data = pipe.get(seller_key)

                # If any of the keys is missing, raise 404
                if not buyer_data:
                    logger.warning(f"Buyer reservation not found for user_id={user_id}, property_id={property_id}")
                    raise HTTPException(status_code=404, detail="Buyer reservation not found")
                if not oh_data:
                    logger.warning(f"Open house event not found for property_id={property_id}")
                    raise HTTPException(status_code=404, detail="Open house event not found")
                if not seller_data:
                    logger.warning(f"Seller reservation not found for user_id={user_id}, property_id={property_id}")
                    raise HTTPException(status_code=404, detail="Seller reservation not found")

                # Parse open house event data
                open_house_event = json.loads(oh_data)
                attendees = open_house_event.get("attendees", 0)

                if attendees <= 0:
                    logger.warning(f"No attendees left to decrement for property_id={property_id}")
                    raise HTTPException(status_code=404, detail="No attendees left to decrement")


                # Begin transaction
                pipe.multi()
                # Remove buyer reservation
                reservations = json.loads(buyer_data)
                updated_reservations = [res for res in reservations if res.get("property_id") != property_id]
                pipe.set(buyer_key, json.dumps(updated_reservations))
                # Decrement attendees
                open_house_event["attendees"] = attendees - 1
                pipe.set(oh_key, json.dumps(open_house_event))
                # Remove seller reservation
                seller_reservations = json.loads(seller_data)
                updated_seller_reservations = [res for res in seller_reservations if res.get("user_id") != user_id]
                pipe.set(seller_key, json.dumps(updated_seller_reservations))

                pipe.execute()
                break
            except WatchError:
                logger.error("WatchError occurred, data changed during transaction.")
                raise HTTPException(status_code=409, detail="Conflict: data changed, please retry.")
            except HTTPException as he:
                raise he
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise HTTPException(status_code=500, detail="Internal server error.")

    # If no exceptions, operation was successful
    logger.info(f"Reservation deleted successfully for user_id={user_id}, property_id={property_id}")
    return KVDBModels.SuccessModel(detail="Reservation deleted successfully")
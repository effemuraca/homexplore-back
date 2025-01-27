import json
from typing import Optional
from entities.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB
from setup.redis_setup.redis_setup import get_redis_client
import logging

# Configura il logger
logger = logging.getLogger(__name__)

class ReservationsBuyerDB:
    reservations_buyer: ReservationsBuyer = None
    
    def __init__(self, reservations_buyer: ReservationsBuyer):
        self.reservations_buyer = reservations_buyer

    def get_reservations_by_user(self, user_id: int) -> Optional[ReservationsBuyer]:
        if not user_id:
            logger.warning("User ID not provided for fetching reservations.")
            return None
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"buyer_id:{user_id}:reservations")
        if not raw_data:
            logger.info(f"No reservations found for user_id={user_id}.")
            return None
        try:
            data = json.loads(raw_data)
            reservation_list = []
            for item in data:
                reservation = ReservationB(
                    property_id=item.get("property_id"),
                    date=item.get("date"),
                    time=item.get("time"),
                    thumbnail=item.get("thumbnail"),
                    address=item.get("address")
                )
                reservation_list.append(reservation)
            self.reservations_buyer = ReservationsBuyer(buyer_id=user_id, reservations=reservation_list)
            return self.reservations_buyer
        except (json.JSONDecodeError, TypeError) as e:
            logger.error(f"Error decoding reservations data: {e}")
            return None

    def delete_reservations_by_user(self, user_id: int) -> bool:
        if not user_id:
            logger.warning("User ID not provided for deletion of reservations.")
            return False
        redis_client = get_redis_client()
        try:
            result = redis_client.delete(f"buyer_id:{user_id}:reservations")
            if result:
                logger.info(f"Reservations deleted for user_id={user_id}.")
            else:
                logger.warning(f"No reservations to delete for user_id={user_id}.")
            return bool(result)
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis error during deletion of reservations: {e}")
            return False

    def create_reservation_buyer(self, user_id: int, reservation: ReservationB) -> bool:
        if not user_id or not reservation:
            logger.warning("User ID or reservation info not provided for creation.")
            return False
        redis_client = get_redis_client()
        try:
            raw_data = redis_client.get(f"buyer_id:{user_id}:reservations")
            if not raw_data:
                data = []
            else:
                data = json.loads(raw_data)
            # Verifica se la prenotazione esiste già
            for res in data:
                if res.get("property_id") == reservation.property_id:
                    logger.info(f"Reservation already exists for user_id={user_id}, property_id={reservation.property_id}.")
                    return False
            # Rimuove la generazione di reservation_id
            reservation_data = {
                "property_id": reservation.property_id,
                "date": reservation.date,
                "time": reservation.time,
                "thumbnail": reservation.thumbnail,
                "address": reservation.address
            }
            data.append(reservation_data)
            result = redis_client.set(f"buyer_id:{user_id}:reservations", json.dumps(data))
            logger.info(f"Reservation created for user_id={user_id}, property_id={reservation.property_id}.")
            return bool(result)
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error creating reservation: {e}")
            return False

    def update_reservation_buyer(self, user_id: int, property_id: int, reservation: ReservationB) -> bool:
        if not user_id or not property_id or not reservation:
            logger.warning("User ID, Property ID, or reservation info not provided for update.")
            return False
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"buyer_id:{user_id}:reservations")
        if not raw_data:
            logger.warning(f"No reservations found for user_id={user_id} to update.")
            return False
        try:
            data = json.loads(raw_data)
            updated = False
            for res in data:
                if res.get("property_id") == property_id:
                    res["date"] = reservation.date if reservation.date is not None else res.get("date")
                    res["time"] = reservation.time if reservation.time is not None else res.get("time")
                    res["thumbnail"] = reservation.thumbnail if reservation.thumbnail is not None else res.get("thumbnail")
                    res["address"] = reservation.address if reservation.address is not None else res.get("address")
                    updated = True
                    break
            if not updated:
                logger.info(f"Reservation not found for user_id={user_id}, property_id={property_id}.")
                return False
            result = redis_client.set(f"buyer_id:{user_id}:reservations", json.dumps(data))
            logger.info(f"Reservation updated for user_id={user_id}, property_id={property_id}.")
            return bool(result)
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error updating reservation: {e}")
            return False

    def delete_reservation_buyer(self, user_id: int, property_id: int) -> bool:
        if not user_id or not property_id:
            logger.warning("User ID or Property ID not provided for deletion of reservation.")
            return False
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"buyer_id:{user_id}:reservations")
        if not raw_data:
            logger.warning(f"No reservations found for user_id={user_id} to delete.")
            return False
        try:
            data = json.loads(raw_data)
            new_data = [res for res in data if res.get("property_id") != property_id]
            if len(new_data) == len(data):
                logger.info(f"Reservation not found for user_id={user_id}, property_id={property_id}.")
                return False
            result = redis_client.set(f"buyer_id:{user_id}:reservations", json.dumps(new_data))
            logger.info(f"Reservation deleted for user_id={user_id}, property_id={property_id}.")
            return bool(result)
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error deleting reservation: {e}")
            return False
import json
from typing import Optional
from entities.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS
from setup.redis_setup.redis_setup import get_redis_client
import logging

# Configura il logger
logger = logging.getLogger(__name__)

class ReservationsSellerDB:
    reservations_seller: ReservationsSeller = None
    
    def __init__(self, reservations_seller: ReservationsSeller):
        self.reservations_seller = reservations_seller

    def get_reservations_seller_by_property_id(self, property_id: int) -> Optional[ReservationsSeller]:
        if not property_id:
            logger.warning("Property ID not provided for fetching seller reservations.")
            return None
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:reservations_seller")
        if not raw_data:
            logger.info(f"No seller reservations found for property_id={property_id}.")
            return None
        try:
            data = json.loads(raw_data)
            reservation_list = []
            for item in data:
                reservation = ReservationS(
                    user_id=item.get("user_id"),
                    full_name=item.get("full_name"),
                    email=item.get("email"),
                    phone=item.get("phone")
                )
                reservation_list.append(reservation)
            self.reservations_seller = ReservationsSeller(property_id=property_id, reservations=reservation_list)
            return self.reservations_seller
        except (json.JSONDecodeError, TypeError) as e:
            logger.error(f"Error decoding seller reservations data: {e}")
            return None

    def delete_reservations_seller_by_property_id_and_user_id(self, property_id: int, user_id: int) -> bool:
        if not property_id or not user_id:
            logger.warning("Property ID or User ID not provided for deleting seller reservation.")
            return False
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:reservations_seller")
        if not raw_data:
            logger.warning(f"No seller reservations found for property_id={property_id}.")
            return False
        try:
            data = json.loads(raw_data)
            new_data = [res for res in data if res.get("user_id") != user_id]
            if len(new_data) == len(data):
                logger.info(f"Seller reservation not found for property_id={property_id}, user_id={user_id}.")
                return False
            result = redis_client.set(f"property_id:{property_id}:reservations_seller", json.dumps(new_data))
            logger.info(f"Seller reservation deleted for property_id={property_id}, user_id={user_id}.")
            return bool(result)
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error deleting seller reservation: {e}")
            return False

    def create_reservation_seller(self, property_id: int, reservation: ReservationS) -> bool:
        if not property_id or not reservation:
            logger.warning("Property ID or reservation info not provided for seller creation.")
            return False
        redis_client = get_redis_client()
        try:
            raw_data = redis_client.get(f"property_id:{property_id}:reservations_seller")
            if not raw_data:
                data = []
            else:
                data = json.loads(raw_data)
            # Verifica se la prenotazione esiste già
            for res in data:
                if res.get("user_id") == reservation.user_id:
                    logger.info(f"Reservation already exists for property_id={property_id}, user_id={reservation.user_id}.")
                    return False
            reservation_data = {
                "user_id": reservation.user_id,
                "full_name": reservation.full_name,
                "email": reservation.email,
                "phone": reservation.phone
            }
            data.append(reservation_data)
            result = redis_client.set(f"property_id:{property_id}:reservations_seller", json.dumps(data))
            logger.info(f"Seller reservation created for property_id={property_id}, user_id={reservation.user_id}.")
            return bool(result)
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error creating seller reservation: {e}")
            return False

    def update_reservation_seller(self, property_id: int, user_id: int, reservation: ReservationS) -> bool:
        if not property_id or not user_id or not reservation:
            logger.warning("Property ID, User ID, or reservation info not provided for update.")
            return False
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:reservations_seller")
        if not raw_data:
            logger.warning(f"No seller reservations found for property_id={property_id} to update.")
            return False
        try:
            data = json.loads(raw_data)
            updated = False
            for res in data:
                if res.get("user_id") == user_id:
                    res["full_name"] = reservation.full_name if reservation.full_name is not None else res.get("full_name")
                    res["email"] = reservation.email if reservation.email is not None else res.get("email")
                    res["phone"] = reservation.phone if reservation.phone is not None else res.get("phone")
                    updated = True
                    break
            if not updated:
                logger.info(f"Seller reservation not found for property_id={property_id}, user_id={user_id}.")
                return False
            result = redis_client.set(f"property_id:{property_id}:reservations_seller", json.dumps(data))
            logger.info(f"Seller reservation updated for property_id={property_id}, user_id={user_id}.")
            return bool(result)
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error updating seller reservation: {e}")
            return False

    def delete_reservation_seller(self, property_id: int, user_id: int) -> bool:
        if not property_id or not user_id:
            logger.warning("Property ID or User ID not provided for deletion of seller reservation.")
            return False
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:reservations_seller")
        if not raw_data:
            logger.warning(f"No seller reservations found for property_id={property_id} to delete.")
            return False
        try:
            data = json.loads(raw_data)
            new_data = [res for res in data if res.get("user_id") != user_id]
            if len(new_data) == len(data):
                logger.info(f"Seller reservation not found for property_id={property_id}, user_id={user_id}.")
                return False
            result = redis_client.set(f"property_id:{property_id}:reservations_seller", json.dumps(new_data))
            logger.info(f"Seller reservation deleted for property_id={property_id}, user_id={user_id}.")
            return bool(result)
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error deleting seller reservation: {e}")
            return False
import json
from typing import Optional
import redis
import logging
from entities.Redis.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS, convert_to_seconds
from setup.redis_setup.redis_setup import get_redis_client

logger = logging.getLogger(__name__)

class ReservationsSellerDB:
    reservations_seller: ReservationsSeller = None

    def __init__(self, reservations_seller: Optional[ReservationsSeller] = None):
        self.reservations_seller = reservations_seller

    def create_reservation_seller(self, day: str, time: str, buyer_id :str, max_reservations : int) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"property_on_sale_id:{self.reservations_seller.property_on_sale_id}:reservations_seller"
        try:
            ttl = convert_to_seconds(day, time)
            # Get existing reservations data from redis
            existing_data = redis_client.get(key)
            if self.reservations_seller.reservations and len(self.reservations_seller.reservations) > 0:
                new_reservation_dict = self.reservations_seller.reservations[0].dict()
            else:
                new_reservation_dict = {"buyer_id": buyer_id}
            
            if existing_data:
                data = json.loads(existing_data)
                reservations_list = data.get("reservations", [])
                # Check if this buyer already has a reservation
                for reservation in reservations_list:
                    if reservation.get("buyer_id") == new_reservation_dict.get("buyer_id"):
                        logger.error("Reservation for this buyer already exists.")
                        return 409
                # Check if max reservations has been reached
                if len(reservations_list) >= max_reservations:
                    logger.error("Max reservations reached.")
                    return 400
                reservations_list.append(new_reservation_dict)
                data["reservations"] = reservations_list
            else:
                # No existing data: use current data from self.reservations_seller
                data = self.reservations_seller.dict()
                data["reservations"] = [new_reservation_dict]
            redis_client.setex(key, ttl, json.dumps(data))
            return 200
        except (redis.exceptions.RedisError, json.JSONDecodeError) as e:
            logger.error(f"Error creating seller reservation: {e}")
            return 500

    def get_reservation_seller(self) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"property_on_sale_id:{self.reservations_seller.property_on_sale_id}:reservations_seller"
        raw_data = redis_client.get(key)
        if not raw_data:
            logger.info(f"No reservations found for property_on_sale_id={self.reservations_seller.property_on_sale_id}.")
            return 404
        try:
            data = json.loads(raw_data)
            self.reservations_seller = ReservationsSeller(
                property_on_sale_id=data.get("property_on_sale_id"),
                reservations=[ReservationS(**item) for item in data.get("reservations", [])]
            )
            return 200
        except (redis.exceptions.RedisError, json.JSONDecodeError, TypeError) as e:
            logger.error(f"Error retrieving seller reservation: {e}")
            return 500

    def update_reservation_seller(self, buyer_id: str, updated_data: dict, new_day: Optional[str] = None) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"property_on_sale_id:{self.reservations_seller.property_on_sale_id}:reservations_seller"
        raw_data = redis_client.get(key)
        if not raw_data:
            logger.warning(f"No reservations found for update on property_on_sale_id={self.reservations_seller.property_on_sale_id}.")
            return 404
        try:
            data = json.loads(raw_data)
            updated = False
            for i, item in enumerate(data.get("reservations", [])):
                if item.get("buyer_id") == buyer_id:
                    data["reservations"][i].update(updated_data)
                    updated = True
                    break
            if not updated:
                logger.warning(f"Reservation for buyer_id={buyer_id} not found.")
                return 404
            redis_client.set(key, json.dumps(data))
            if new_day and updated_data.get("time"):
                ttl = convert_to_seconds(new_day, updated_data.get("time"))
                if ttl:
                    redis_client.expire(key, ttl)
            return 200
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error updating seller reservation: {e}")
            return 500

    def delete_reservation_seller_by_buyer_id(self, buyer_id: str) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"property_on_sale_id:{self.reservations_seller.property_on_sale_id}:reservations_seller"
        raw_data = redis_client.get(key)
        if not raw_data:
            logger.warning("No reservations found for deletion.")
            return 404
        try:
            data = json.loads(raw_data)
            new_list = [item for item in data.get("reservations", []) if item.get("buyer_id") != buyer_id]
            data["reservations"] = new_list
            redis_client.set(key, json.dumps(data))
            return 200
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error deleting seller reservation by buyer_id: {e}")
            return 500

    def delete_entire_reservation_seller(self) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"property_on_sale_id:{self.reservations_seller.property_on_sale_id}:reservations_seller"
        try:
            redis_client.delete(key)
            return 200
        except redis.exceptions.RedisError as e:
            logger.error(f"Error deleting entire seller reservation: {e}")
            return 500
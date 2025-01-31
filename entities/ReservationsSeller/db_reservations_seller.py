import logging
import json
import redis
from typing import Optional, List
from entities.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS, convert_to_seconds
from setup.redis_setup.redis_setup import get_redis_client

logger = logging.getLogger(__name__)

class ReservationsSellerDB:
    reservations_seller: ReservationsSeller = None

    def __init__(self, reservations_seller: ReservationsSeller, area: Optional[int] = None):
        self.reservations_seller = reservations_seller
        self.area = area
        if self.area is not None:
            self.reservations_seller.max_reservations = ReservationsSeller.calculate_max_reservations(self.area)

    def create_reservation_seller(self, day: str, time: str) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"property_id:{self.reservations_seller.property_id}:reservations_seller"
        try:
            existing_data = redis_client.get(key)
            reservations = self.reservations_seller.reservations or []
            if existing_data:
                data = json.loads(existing_data)
                # Check for duplicate reservation
                for res in data:
                    if res.get("buyer_id") == self.reservations_seller.reservations[0].buyer_id:
                        logger.warning("Duplicate seller reservation detected.")
                        return 409
                # Check max_reservations
                if len(data) + len(reservations) > self.reservations_seller.max_reservations:
                    logger.error("Maximum reservations exceeded.")
                    return 400
                data.extend([res.dict() for res in reservations])
                redis_client.set(key, json.dumps(data))
            else:
                # Check max_reservations
                if len(reservations) > self.reservations_seller.max_reservations:
                    logger.error("Maximum reservations exceeded.")
                    return 400
                data = [res.dict() for res in reservations]
                redis_client.set(key, json.dumps(data))
            return 200
        except (redis.exceptions.RedisError, json.JSONDecodeError) as e:
            logger.error(f"Error creating seller reservation: {e}")
            return 500

    def get_reservation_seller(self) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"property_id:{self.reservations_seller.property_id}:reservations_seller"
        raw_data = redis_client.get(key)
        if not raw_data:
            logger.info(f"No seller reservations found for property_id={self.reservations_seller.property_id}.")
            return 404
        try:
            data = json.loads(raw_data)
            reservation_list = [ReservationS(**item) for item in data]
            self.reservations_seller.reservations = reservation_list
            self.reservations_seller.total_reservations = len(reservation_list)
            return 200
        except (json.JSONDecodeError, TypeError) as e:
            logger.error(f"Error decoding seller reservations data: {e}")
            return 500

    def update_reservation_seller(self, buyer_id: str, updated_data: dict) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"property_id:{self.reservations_seller.property_id}:reservations_seller"
        raw_data = redis_client.get(key)
        if not raw_data:
            logger.warning(f"No seller reservations found for property_id={self.reservations_seller.property_id}.")
            return 404
        try:
            data = json.loads(raw_data)
            for res in data:
                if res.get("buyer_id") == buyer_id:
                    res.update(updated_data)
                    redis_client.set(key, json.dumps(data))
                    logger.info(f"Reservation for buyer_id={buyer_id} updated successfully.")
                    return 200
            logger.info(f"Reservation not found for buyer_id={buyer_id}.")
            return 404
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error updating seller reservation: {e}")
            return 500

    def update_entire_reservation_seller(self, new_data: List[ReservationS], area: Optional[int] = None) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"property_id:{self.reservations_seller.property_id}:reservations_seller"
        try:
            if area is not None:
                self.reservations_seller.area = area
                self.reservations_seller.max_reservations = ReservationsSeller.calculate_max_reservations(area)
            if len(new_data) > self.reservations_seller.max_reservations:
                logger.error("Number of reservations exceeds maximum allowed.")
                return 400
            reservations_dict = [r.dict() for r in new_data]
            redis_client.set(key, json.dumps(reservations_dict))
            logger.info(f"Entire ReservationSeller record updated for property_id={self.reservations_seller.property_id}.")
            return 200
        except redis.exceptions.RedisError as e:
            logger.error(f"Error updating entire ReservationSeller record: {e}")
            return 500

    def delete_reservation_seller_by_buyer_id(self, buyer_id: str) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"property_id:{self.reservations_seller.property_id}:reservations_seller"
        raw_data = redis_client.get(key)
        if not raw_data:
            logger.warning(f"No seller reservations found for property_id={self.reservations_seller.property_id}.")
            return 404
        try:
            data = json.loads(raw_data)
            new_data = [res for res in data if res.get("buyer_id") != buyer_id]
            if len(new_data) == len(data):
                logger.info(f"Seller reservation not found for buyer_id={buyer_id}.")
                return 404
            redis_client.set(key, json.dumps(new_data))
            logger.info(f"Seller reservation deleted for buyer_id={buyer_id}.")
            return 200
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error deleting seller reservation: {e}")
            return 500

    def delete_entire_reservation_seller(self) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"property_id:{self.reservations_seller.property_id}:reservations_seller"
        try:
            if not redis_client.exists(key):
                logger.warning(f"No seller reservations to delete for property_id={self.reservations_seller.property_id}.")
                return 404
            redis_client.delete(key)
            logger.info(f"All seller reservations deleted for property_id={self.reservations_seller.property_id}.")
            return 200
        except redis.exceptions.RedisError as e:
            logger.error(f"Error deleting entire ReservationSeller record: {e}")
            return 500
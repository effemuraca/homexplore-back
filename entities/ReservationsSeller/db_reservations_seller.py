from typing import Optional, List
from entities.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS
import redis
from setup.redis_setup.redis_setup import get_redis_client
import json
import logging

# Configura il logger
logger = logging.getLogger(__name__)

class ReservationsSellerDB:
    reservations_seller: ReservationsSeller = None
    
    def __init__(self, reservations_seller: ReservationsSeller):
        self.reservations_seller = reservations_seller

    def create_reservation_seller(self, seconds: int) -> int:
        if not self.reservations_seller:
            logger.error("No reservations_seller data provided.")
            return 400
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        try:
            key = f"property_id:{self.reservations_seller.property_id}:reservations_seller"
            raw_data = redis_client.get(key)
            if raw_data:
                logger.info("Reservation already exists.")
                return 409
            data = [r.dict() for r in self.reservations_seller.reservations or []]
            redis_client.setex(key, seconds, json.dumps(data))
            logger.info("Seller reservation created.")
            return 201
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error creating seller reservation: {e}")
            return 500

    def get_reservations_seller_by_property_id(self) -> int:
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
            self.reservations_seller = ReservationsSeller(property_id=self.reservations_seller.property_id, reservations=reservation_list)
            return 200
        except (json.JSONDecodeError, TypeError) as e:
            logger.error(f"Error decoding seller reservations data: {e}")
            return 500

    def update_reservation_seller(self) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        raw_data = redis_client.get(f"property_id:{self.reservations_seller.property_id}:reservations_seller")
        if not raw_data:
            logger.warning(f"No seller reservations found for property_id={self.reservations_seller.property_id} to update.")
            return 404
        try:
            data = json.loads(raw_data)
            updated = False
            reservation_to_update = self.reservations_seller.reservations[0]
            for res in data:
                existing_reservation = ReservationS(**res)
                if existing_reservation.buyer_id == reservation_to_update.buyer_id:
                    updated_reservation = reservation_to_update.dict(exclude_unset=True)
                    res.update(updated_reservation)
                    updated = True
                    break
            if not updated:
                logger.info(f"Reservation not found for property_id={self.reservations_seller.property_id}, buyer_id={reservation_to_update.buyer_id}.")
                return 404
            result = redis_client.set(f"property_id:{self.reservations_seller.property_id}:reservations_seller", json.dumps(data))
            logger.info(f"Seller reservation updated for property_id={self.reservations_seller.property_id}, buyer_id={reservation_to_update.buyer_id}.")
            if result:
                return 200
            return 500
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error updating seller reservation: {e}")
            return 500

    def delete_reservations_seller(self) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        result = redis_client.delete(f"property_id:{self.reservations_seller.property_id}:reservations_seller")
        if result:
            logger.info(f"Reservations deleted for property_id={self.reservations_seller.property_id}.")
            return 200
        logger.warning(f"No reservations found for property_id={self.reservations_seller.property_id} or delete failed.")
        return 404
            
    def delete_reservation_seller_by_property_id_and_buyer_id(self, buyer_id: str) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        raw_data = redis_client.get(f"property_id:{self.reservations_seller.property_id}:reservations_seller")
        if not raw_data:
            logger.warning(f"No seller reservations found for property_id={self.reservations_seller.property_id}.")
            return 404
        try:
            data = json.loads(raw_data)
            new_data = [res for res in data if res.get("buyer_id") != buyer_id]
            if len(new_data) == len(data):
                logger.info(f"Seller reservation not found for property_id={self.reservations_seller.property_id}, buyer_id={buyer_id}.")
                return 404
            result = redis_client.set(f"property_id:{self.reservations_seller.property_id}:reservations_seller", json.dumps(new_data))
            logger.info(f"Seller reservation deleted for property_id={self.reservations_seller.property_id}, buyer_id={buyer_id}.")
            if result:
                return 200
            return 500
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error deleting seller reservation: {e}")
            return 500
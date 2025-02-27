from typing import Optional, List
from entities.Redis.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB
from setup.redis_setup.redis_setup import get_redis_client
import json
import redis
import logging

# Configure logger
logger = logging.getLogger(__name__)

class ReservationsBuyerDB:
    reservations_buyer: ReservationsBuyer = None
    
    def __init__(self, reservations_buyer: Optional[ReservationsBuyer] = None):
        self.reservations_buyer = reservations_buyer
  
    def create_reservation_buyer(self) -> int:
        """
        Create a new reservation for this buyer in Redis.

        Returns:
            int:
                201 if the reservation is created successfully,
                500 if there's a Redis or JSON decoding error.
        """
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"buyer_id:{self.reservations_buyer.buyer_id}:reservations_buyer"
        try:
            existing_data = redis_client.get(key)
            new_reservations = [res.model_dump() if hasattr(res, "dict") else res for res in (self.reservations_buyer.reservations or [])]
            if existing_data:
                stored = json.loads(existing_data)
                reservations = stored + new_reservations
            else:
                reservations = new_reservations
            redis_client.set(key, json.dumps(reservations))
            return 201
        except (redis.exceptions.RedisError, json.JSONDecodeError) as e:
            logger.error(f"Error creating buyer reservation for buyer_id={self.reservations_buyer.buyer_id}: {e}")
            return 500
            
    def get_reservations_by_user(self) -> int:
        """
        Retrieve all reservations for this buyer from Redis.

        Returns:
            int:
                200 if the reservations are retrieved,
                404 if no data is found,
                500 if there's a Redis or JSON decoding error.
        """
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"buyer_id:{self.reservations_buyer.buyer_id}:reservations_buyer"
        raw_data = redis_client.get(key)
        if not raw_data:
            return 404
        try:
            data = json.loads(raw_data)
            reservation_list = [ReservationB(**item) for item in data]
            self.reservations_buyer = ReservationsBuyer(buyer_id=self.reservations_buyer.buyer_id, reservations=reservation_list)
            return 200
        except (json.JSONDecodeError, TypeError) as e:
            logger.error(f"Error decoding reservations data for buyer_id={self.reservations_buyer.buyer_id}: {e}")
            return 500

    def update_reservation_buyer(self) -> int:
        """
        Update a reservation for this buyer in Redis.

        Returns:
            int:
                200 if the reservation is updated,
                404 if no matching reservation is found,
                400 if reservations_buyer is not provided,
                500 if there's a Redis or JSON decoding error.
        """
        if not self.reservations_buyer:
            return 400
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"buyer_id:{self.reservations_buyer.buyer_id}:reservations_buyer"
        try:
            raw_data = redis_client.get(key)
            if not raw_data:
                return 404
            data = json.loads(raw_data)
            updated = False
            reservation_to_update = self.reservations_buyer.reservations[0]
            for idx, res in enumerate(data):
                if res.get("property_on_sale_id") == reservation_to_update.property_on_sale_id:
                    data[idx] = reservation_to_update.model_dump()
                    updated = True
                    break
            if not updated:
                return 404
            redis_client.set(key, json.dumps(data))
            return 200
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error updating reservation for buyer_id={self.reservations_buyer.buyer_id}: {e}")
            return 500

    def delete_reservations_buyer(self) -> int:
        """
        Delete all reservations for this buyer in Redis.

        Returns:
            int:
                200 if the reservations are deleted,
                404 if no reservations exist,
                500 if there's a Redis error.
        """
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        try:
            key = f"buyer_id:{self.reservations_buyer.buyer_id}:reservations_buyer"
            result = redis_client.delete(key)
            if result:
                return 200
            else:
                return 404
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis error during deletion of reservations for buyer_id={self.reservations_buyer.buyer_id}: {e}")
            return 500
    
    def delete_reservation_by_property_on_sale_id(self, property_on_sale_id: str) -> int:
        """
        Delete a reservation for a specific property_on_sale_id.

        Args:
            property_on_sale_id (str): The property_on_sale_id to delete.

        Returns:
            int:
                200 if the reservation is deleted,
                404 if no reservation is found for that property_on_sale_id,
                500 if there's a Redis or JSON decoding error.
        """
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        try:
            key = f"buyer_id:{self.reservations_buyer.buyer_id}:reservations_buyer"
            raw_data = redis_client.get(key)
            if not raw_data:
                return 404
            data = json.loads(raw_data)
            new_data = [res for res in data if res.get("property_on_sale_id") != property_on_sale_id]
            if len(new_data) == len(data):
                return 404
            result = redis_client.set(key, json.dumps(new_data))
            if result:
                return 200
            logger.error(f"Error deleting reservation for buyer_id={self.reservations_buyer.buyer_id}.")
            return 500
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error deleting reservation for buyer_id={self.reservations_buyer.buyer_id}: {e}")
            return 500

    def update_expired_reservations(self) -> int:
        """
        Remove all expired reservations for this buyer in Redis.

        Returns:
            int:
                200 if expired reservations are removed or there are none,
                404 if no reservations are found,
                500 if there's a Redis or JSON decoding error.
        """
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"buyer_id:{self.reservations_buyer.buyer_id}:reservations_buyer"
        raw_data = redis_client.get(key)
        if not raw_data:
            return 404
        try:
            data = json.loads(raw_data)
            new_data = [res for res in data if not ReservationB(**res).check_reservation_expired()]
            # The update is performed only if there are expired reservations
            if len(new_data) != len(data):
                redis_client.set(key, json.dumps(new_data))
            self.reservations_buyer.reservations = new_data
            return 200
        except (json.JSONDecodeError, TypeError) as e:
            logger.error(f"Error updating expired reservations for buyer_id={self.reservations_buyer.buyer_id}: {e}")
            return 500
import json
from typing import Optional
import redis
import logging
from entities.Redis.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS, convert_to_seconds
from setup.redis_setup.redis_setup import get_redis_client

# Configure logger
logger = logging.getLogger(__name__)

class ReservationsSellerDB:
    reservations_seller: ReservationsSeller = None

    def __init__(self, reservations_seller: Optional[ReservationsSeller] = None):
        self.reservations_seller = reservations_seller

    def create_reservation_seller(self, day: str, time: str, buyer_id :str, max_attendees : int) -> int:
        """
        Create a new reservation for this property_on_sale_id, associating it to a buyer.

        Args:
            day (str): The day of the reservation.
            time (str): The time of the reservation.
            buyer_id (str): The ID of the buyer creating this reservation.
            max_attendees (int): The maximum number of reservations allowed

        Returns:
            int: 200 if the reservation was created successfully, 
                 409 if the buyer already has a reservation, 
                 400 if max_attendees has been reached,
                 500 if there's an internal error.
        """
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
                new_reservation_dict = self.reservations_seller.reservations[0].model_dump()
            else:
                new_reservation_dict = {"buyer_id": buyer_id}
            
            if existing_data:
                data = json.loads(existing_data)
                reservations_list = data
                # Check if this buyer already has a reservation
                for reservation in reservations_list:
                    if reservation.get("buyer_id") == new_reservation_dict.get("buyer_id"):
                        return 409
                # Check if max reservations has been reached
                if len(reservations_list) >= max_attendees:
                    return 400
                reservations_list.append(new_reservation_dict)
                data = reservations_list
            else:
                # No existing data: use current data from self.reservations_seller
                data = self.reservations_seller.model_dump()
                data = [new_reservation_dict]
            redis_client.setex(key, ttl, json.dumps(data))
            return 200
        except (redis.exceptions.RedisError, json.JSONDecodeError) as e:
            logger.error(f"Error creating seller reservation for property_on_sale_id={self.reservations_seller.property_on_sale_id}: {e}")
            return 500

    def get_reservation_seller(self) -> int:
        """
        Retrieve the reservation data for this property_on_sale_id from Redis.

        Returns:
            int: 200 if the data is retrieved successfully,
                 404 if no data is found,
                 500 if there is an internal error.
        """
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"property_on_sale_id:{self.reservations_seller.property_on_sale_id}:reservations_seller"
        raw_data = redis_client.get(key)
        if not raw_data:
            return 404
        try:
            data = json.loads(raw_data)
            self.reservations_seller = ReservationsSeller(
                property_on_sale_id=self.reservations_seller.property_on_sale_id,
                reservations=[
                    ReservationS(**{k: v for k, v in item.items() if k != "buyer_id"})
                    for item in data
                ]
            )
            return 200
        except (redis.exceptions.RedisError, json.JSONDecodeError, TypeError) as e:
            logger.error(f"Error retrieving seller reservation for property_on_sale_id={self.reservations_seller.property_on_sale_id}: {e}")
            return 500

    def update_reservation_seller(self, buyer_id: str, updated_data: dict) -> int:
        """
        Update an existing reservation for a specific buyer on this property_on_sale_id.

        Args:
            buyer_id (str): The buyer's ID whose reservation needs to be updated.
            updated_data (dict): The data to update.

        Returns:
            int: 200 if the reservation is updated successfully, 
                 404 if the reservation or buyer is not found,
                 500 if there is an internal error.
        """
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"property_on_sale_id:{self.reservations_seller.property_on_sale_id}:reservations_seller"
        raw_data = redis_client.get(key)
        if not raw_data:
            return 404
        try:
            data = json.loads(raw_data)
            updated = False
            for i, item in enumerate(data):
                if item.get("buyer_id") == buyer_id:
                    data[i].update(updated_data)
                    updated = True
                    break
            if not updated:
                return 404
            return 200
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error updating seller reservation with buyer_id={buyer_id}: {e}")
            return 500

    def delete_reservation_seller_by_buyer_id(self, buyer_id: str) -> int:
        """
        Delete a reservation for a specific buyer from this property_on_sale_id.

        Args:
            buyer_id (str): The buyer's ID whose reservation needs to be deleted.

        Returns:
            int: 200 if the reservation is deleted,
                 404 if the reservation or buyer is not found,
                 500 if there is an internal error.
        """
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"property_on_sale_id:{self.reservations_seller.property_on_sale_id}:reservations_seller"
        raw_data = redis_client.get(key)
        if not raw_data:
            return 404
        try:
            data = json.loads(raw_data)
            new_list = [item for item in data if item.get("buyer_id") != buyer_id]
            data = new_list
            redis_client.set(key, json.dumps(data))
            return 200
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error deleting seller reservation with buyer_id={buyer_id}: {e}")
            return 500

    def delete_entire_reservation_seller(self) -> int:
        """
        Delete all reservation data for this property_on_sale_id.

        Returns:
            int: 200 if the reservation data is deleted successfully,
                 500 if there is an internal error.
        """
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"property_on_sale_id:{self.reservations_seller.property_on_sale_id}:reservations_seller"
        try:
            redis_client.delete(key)
            return 200
        except redis.exceptions.RedisError as e:
            logger.error(f"Error deleting entire seller reservation for property_on_sale_id={self.reservations_seller.property_on_sale_id}: {e}")
            return 500
        
    def update_day_and_time(self, day: str, time: str) -> int:
        """
        Update the TTL (day and time) of the seller's reservation data for this property_on_sale_id.

        Args:
            day (str): The new day of the reservation.
            time (str): The new time of the reservation.

        Returns:
            int: 200 if the TTL is updated successfully,
                 404 if no data is found,
                 500 if there is an internal error.
        """
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"property_on_sale_id:{self.reservations_seller.property_on_sale_id}:reservations_seller"
        try:
            ttl = convert_to_seconds(day, time)
            raw_data = redis_client.get(key)
            if not raw_data:
                return 404
            redis_client.expire(key, ttl)
            return 200
        except (redis.exceptions.RedisError, json.JSONDecodeError) as e:
            logger.error(f"Error updating day and time for property_on_sale_id={self.reservations_seller.property_on_sale_id}: {e}")
            return 500
        
    def handle_book_now_transaction(self, reservation: ReservationS, day: str, time: str, buyer_id: str, max_attendees: int) -> int:
        """
        Handle a new reservation in a transactional way to avoid concurrency issues,
        linking it to this property_on_sale_id.

        Args:
            reservation (ReservationS): The reservation details to store.
            day (str): The day of the reservation.
            time (str): The time of the reservation.
            buyer_id (str): The ID of the buyer making the reservation.
            max_attendees (int): The max number of allowed reservations.

        Returns:
            int: 200 if the transaction succeeds, 
                 400 if max_attendees is reached or day/time is invalid, 
                 409 if the buyer already has a reservation,
                 500 if there's a concurrency or Redis error.
        """
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"property_on_sale_id:{self.reservations_seller.property_on_sale_id}:reservations_seller"
        ttl = convert_to_seconds(day, time)
        if ttl is None:
            return 400

        try:
            with redis_client.pipeline() as pipe:
                # Watch the key to detect concurrent modifications
                pipe.watch(key)

                # Retrieve the data BEFORE starting the transaction
                raw_data = pipe.get(key)
                reservations_list = json.loads(raw_data) if raw_data else []

                # Check max attendees
                if len(reservations_list) >= max_attendees:
                    pipe.unwatch()
                    return 400

                # Append new reservation
                reservations_list.append(reservation.model_dump())

                # Start transaction
                pipe.multi()
                pipe.setex(key, ttl, json.dumps(reservations_list))
                pipe.execute()
                return 200
        except redis.exceptions.WatchError:
            logger.error(f"Transaction conflict on key={key}.")
            return 500
        except (redis.exceptions.RedisError, json.JSONDecodeError) as e:
            logger.error(f"Error in handle_book_now_transaction: {e}")
            return 500
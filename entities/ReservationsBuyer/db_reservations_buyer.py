from typing import Optional, List
from entities.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB
from setup.redis_setup.redis_setup import get_redis_client
import json
import redis
import logging

# Configura il logger
logger = logging.getLogger(__name__)

class ReservationsBuyerDB:
    reservations_buyer: ReservationsBuyer = None
    
    def __init__(self, reservations_buyer: Optional[ReservationsBuyer] = None):
        self.reservations_buyer = reservations_buyer
  
    def create_reservation_buyer(self) -> int:
        if not self.reservations_buyer:
            logger.error("No reservations_buyer data provided.")
            return 400
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        try:
            key = f"buyer_id:{self.reservations_buyer.buyer_id}:reservations"
            raw_data = redis_client.get(key)
            if raw_data:
                data = json.loads(raw_data)
                # Verifica se la prenotazione esiste già
                for res in data:
                    if res['property_id'] == self.reservations_buyer.reservations[0].property_id:
                        logger.info("Reservation already exists.")
                        return 409
            else:
                data = []
            # Aggiungi nuova prenotazione
            reservation = self.reservations_buyer.reservations[0].dict()
            data.append(reservation)
            # Salva in Redis con scadenza
            redis_client.set(key, json.dumps(data))
            logger.info(f"Reservation created for buyer_id={self.reservations_buyer.buyer_id}, property_id={self.reservations_buyer.reservations[0].property_id}.")
            return 201
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error creating reservation: {e}")
            return 500

            
    def get_reservations_by_user(self) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"buyer_id:{self.reservations_buyer.buyer_id}:reservations"
        raw_data = redis_client.get(key)
        if not raw_data:
            logger.info(f"No reservations found for buyer_id={self.reservations_buyer.buyer_id}.")
            return 404
        try:
            data = json.loads(raw_data)
            reservation_list = [ReservationB(**item) for item in data]
            self.reservations_buyer = ReservationsBuyer(buyer_id=self.reservations_buyer.buyer_id, reservations=reservation_list)
            return 200
        except (json.JSONDecodeError, TypeError) as e:
            logger.error(f"Error decoding reservations data: {e}")
            return 500

    def update_reservation_buyer(self) -> int:
        if not self.reservations_buyer:
            logger.error("No reservations_buyer data provided for update.")
            return 400
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        key = f"buyer_id:{self.reservations_buyer.buyer_id}:reservations"
        try:
            raw_data = redis_client.get(key)
            if not raw_data:
                logger.warning(f"No reservations found for buyer_id={self.reservations_buyer.buyer_id} to update.")
                return 404
            data = json.loads(raw_data)
            updated = False
            reservation_to_update = self.reservations_buyer.reservations[0]
            for idx, res in enumerate(data):
                if res['property_id'] == reservation_to_update.property_id:
                    data[idx] = reservation_to_update.dict()
                    updated = True
                    break
            if not updated:
                logger.info(f"Reservation with property_id={reservation_to_update.property_id} not found.")
                return 404
            redis_client.set(key, json.dumps(data))
            logger.info(f"Reservation updated for buyer_id={self.reservations_buyer.buyer_id}, property_id={reservation_to_update.property_id}.")
            return 200
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error updating reservation: {e}")
            return 500

    def delete_reservations_buyer(self) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        try:
            key = f"buyer_id:{self.reservations_buyer.buyer_id}:reservations"
            result = redis_client.delete(key)
            if result:
                logger.info(f"All reservations deleted for buyer_id={self.reservations_buyer.buyer_id}.")
                return 200
            else:
                logger.info(f"No reservations found to delete for buyer_id={self.reservations_buyer.buyer_id}.")
                return 404
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis error during deletion of reservations: {e}")
            return 500
    
    def delete_reservation_by_property_id(self, property_id: str) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        try:
            key = f"buyer_id:{self.reservations_buyer.buyer_id}:reservations"
            raw_data = redis_client.get(key)
            if not raw_data:
                logger.warning(f"No reservations found for buyer_id={self.reservations_buyer.buyer_id} to delete.")
                return 404
            data = json.loads(raw_data)
            new_data = [res for res in data if res.get("property_id") != property_id]
            if len(new_data) == len(data):
                logger.info(f"Reservation with property_id={property_id} not found for buyer_id={self.reservations_buyer.buyer_id}.")
                return 404
            result = redis_client.set(key, json.dumps(new_data))
            logger.info(f"Reservation with property_id={property_id} deleted for buyer_id={self.reservations_buyer.buyer_id}.")
            if result:
                return 200
            return 500
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error deleting reservation: {e}")
            return 500
        
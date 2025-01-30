from typing import Optional, List
from entities.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB
from setup.redis_setup.redis_setup import get_redis_client
import json
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
            raw_data = redis_client.get(f"buyer_id:{self.reservations_buyer.buyer_id}:reservations")
            if not raw_data:
                data = []
            else:
                data = json.loads(raw_data)
            
                # Verifica se la prenotazione esiste già
                for res in data:
                    existing_reservation = ReservationB(**res)
                    if existing_reservation.property_id == reservation.property_id:
                        logger.info(f"Reservation already exists for buyer_id={self.reservations_buyer.buyer_id}, property_id={existing_reservation.property_id}.")
                        return 409

                # Utilizza la classe ReservationB invece del dizionario
                reservation = self.reservations_buyer.reservations[0]
                reservation_data = reservation.dict()
                data.append(reservation_data)
                result = redis_client.set(f"buyer_id:{self.reservations_buyer.buyer_id}:reservations", json.dumps([res.dict() for res in data]))
                logger.info(f"Reservation created for buyer_id={self.reservations_buyer.buyer_id}, property_id={self.reservations_buyer.reservations[0].property_id}.")
                if result:
                    return 201
                return 500
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error creating reservation: {e}")
            return 500
            
    def get_reservations_by_user(self) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
            
        raw_data = redis_client.get(f"buyer_id:{self.reservations_buyer.buyer_id}:reservations")
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
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        raw_data = redis_client.get(f"buyer_id:{self.reservations_buyer.buyer_id}:reservations")
        if not raw_data:
            logger.warning(f"No reservations found for buyer_id={self.reservations_buyer.buyer_id} to update.")
            return 404
        try:
            data = json.loads(raw_data)
            updated = False
            reservation_to_update = self.reservations_buyer.reservations[0]
            for res in data:
                existing_reservation = ReservationB(**res)
                if existing_reservation.property_id == reservation_to_update.property_id:
                    updated_reservation = reservation_to_update.dict(exclude_unset=True)
                    res.update(updated_reservation)
                    updated = True
                    break
            if not updated:
                logger.info(f"Reservation not found for buyer_id={self.reservations_buyer.buyer_id}, property_id={reservation_to_update.property_id}.")
                return 404
            result = redis_client.set(f"buyer_id:{self.reservations_buyer.buyer_id}:reservations", json.dumps(data))
            logger.info(f"Reservation updated for buyer_id={self.reservations_buyer.buyer_id}, property_id={reservation_to_update.property_id}.")
            if result:
                return 200
            return 500
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error updating reservation: {e}")
            return 500

    def delete_reservations_by_user(self) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        try:
            result = redis_client.delete(f"buyer_id:{self.reservations_buyer.buyer_id}:reservations")
            if result:
                logger.info(f"All reservations deleted for buyer_id={self.reservations_buyer.buyer_id}.")
                return 200
            else:
                logger.warning(f"Failed to delete reservations for buyer_id={self.reservations_buyer.buyer_id}.")
                return 404
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis error during deletion of reservations: {e}")
            return 500
    
    def delete_reservation_buyer(self) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        raw_data = redis_client.get(f"buyer_id:{self.reservations_buyer.buyer_id}:reservations")
        if not raw_data:
            logger.warning(f"No reservations found for buyer_id={self.reservations_buyer.buyer_id} to delete.")
            return 404

        try:
            data = json.loads(raw_data)
            property_id = self.reservations_buyer.reservations[0].property_id
            new_data = [res for res in data if res.get("property_id") != property_id]
            if len(new_data) == len(data):
                logger.info(f"Reservation not found for buyer_id={self.reservations_buyer.buyer_id}, property_id={property_id}.")
                return 404
            result = redis_client.set(f"buyer_id:{self.reservations_buyer.buyer_id}:reservations", json.dumps(new_data))
            logger.info(f"Reservation deleted for buyer_id={self.reservations_buyer.buyer_id}, property_id={property_id}.")
            if result:
                return 200
            return 500
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error deleting reservation: {e}")
            return 500
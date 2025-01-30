from typing import Optional, List
from entities.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS
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
            raw_data = redis_client.get(f"property_id:{self.reservations_seller.property_id}:reservations_seller")
            if not raw_data:
                data = []
            else:
                data = json.loads(raw_data)
            
             #Verifica se la prenotazione esiste già
                for res in data:
                    existing_reservation = ReservationS(**res)
                    if existing_reservation.buyer_id == reservation.buyer_id:
                        logger.info(f"Reservation already exists for property_id={self.reservations_seller.property_id}, buyer_id={existing_reservation.buyer_id}.")
                        return 409

                # Utilizza la classe ReservationS invece del dizionario
                reservation = self.reservations_seller.reservations[0]
                reservation_data = reservation.dict()
                data.append(reservation_data)
                result = redis_client.set(f"property_id:{self.reservations_seller.property_id}:reservations_seller", json.dumps([res.dict() for res in data]))
                logger.info(f"Seller reservation created for property_id={self.reservations_seller.property_id}, buyer_id={self.reservations_seller.reservations[0].buyer_id}.")
                if not result:
                    return 500
                result = redis_client.expire(f"property_id:{self.reservations_seller.property_id}:reservations_seller", seconds)
                if not result:
                    logger.error(f"Failed to set expiration for reservations_seller of property_id={self.reservations_seller.property_id}.")
                    return 500
                return 201
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error creating seller reservation: {e}")
            return 500

    def get_reservations_seller_by_property_id(self) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        raw_data = redis_client.get(f"property_id:{self.reservations_seller.property_id}:reservations_seller")
        if not raw_data:
            logger.info(f"No seller reservations found for property_id={self.reservations_seller.property_id}.")
            return 404
        try:
            data = json.loads(raw_data)
            reservation_list = []
            for item in data:
                reservation = ReservationS(
                    buyer_id=item.get("buyer_id"),
                    full_name=item.get("full_name"),
                    email=item.get("email"),
                    phone=item.get("phone")
                )
                reservation_list.append(reservation)
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

    def delete_reservation_seller(self) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.error("Failed to connect to Redis.")
            return 500
        raw_data = redis_client.get(f"property_id:{self.reservations_seller.property_id}:reservations_seller")
        if not raw_data:
            logger.warning(f"No seller reservations found for property_id={self.reservations_seller.property_id} to delete.")
            return 404
        try:
            data = json.loads(raw_data)
            buyer_id = self.reservations_seller.reservations[0].buyer_id
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
            
    def delete_reservations_seller_by_property_id_and_buyer_id(self, buyer_id: str) -> int:
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
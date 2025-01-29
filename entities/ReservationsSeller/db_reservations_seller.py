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

    def create_reservation_seller(self, seconds:int) -> int:
        if not self.reservations_seller:
            return 400
        redis_client = get_redis_client()
        if redis_client is None:
            return 500
        try:
            raw_data = redis_client.get(f"property_id:{self.reservations_seller.property_id}:reservations_seller")
            if not raw_data:
                data = []
            else:
                data = json.loads(raw_data)
            # Verifica se la prenotazione esiste già
            for res in data:
                if res.get("buyer_id") == self.reservations_seller.reservations[0].buyer_id:
                    logger.info(f"Reservation already exists for property_id={self.reservations_seller.property_id}, buyer_id={self.reservations_seller.reservations.buyer_id}.")
                    return 409
            reservation = self.reservations_seller.reservations[0]
            reservation_data = {
                "buyer_id": reservation.buyer_id,
                "full_name": reservation.full_name,
                "email": reservation.email,
                "phone": reservation.phone
            }
            data.append(reservation_data)
            result = redis_client.set(f"property_id:{self.reservations_seller.property_id}:reservations_seller", json.dumps(data))
            logger.info(f"Seller reservation created for property_id={self.reservations_seller.property_id}, buyer_id={self.reservations_seller.reservations.buyer_id}.")
            if not result:
                return 500
            result = redis_client.expire(f"property_id:{self.reservations_seller.property_id}:reservations_seller", seconds)
            if not result:
                return 500
            return 201
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error creating seller reservation: {e}")
            return 500

    def get_reservations_seller_by_property_id(self) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
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
                if res.get("buyer_id") == reservation_to_update.buyer_id:
                    res["full_name"] = reservation_to_update.full_name if reservation_to_update.full_name is not None else res.get("full_name")
                    res["email"] = reservation_to_update.email if reservation_to_update.email is not None else res.get("email")
                    res["phone"] = reservation_to_update.phone if reservation_to_update.phone is not None else res.get("phone")
                    updated = True
                    break
            if not updated:
                logger.info(f"Seller reservation not found for property_id={self.reservations_seller.property_id}, buyer_id={self.reservations_seller.reservations.buyer_id}.")
                return 404
            result = redis_client.set(f"property_id:{self.reservations_seller.property_id}:reservations_seller", json.dumps(data))
            logger.info(f"Seller reservation updated for property_id={self.reservations_seller.property_id}, buyer_id={self.reservations_seller.reservations.buyer_id}.")
            if not result:
                return 500
            return 200
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error updating seller reservation: {e}")
            return 500

    def delete_reservation_seller(self) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            return 500
        raw_data = redis_client.get(f"property_id:{self.reservations_seller.property_id}:reservations_seller")
        if not raw_data:
            logger.warning(f"No seller reservations found for property_id={self.reservations_seller.property_id} to delete.")
            return 404
        try:
            buyer_id = self.reservations_seller.reservations[0].buyer_id
            new_data = [res for res in data if res.get("buyer_id") != buyer_id]
            if len(new_data) == len(data):
                logger.info(f"Seller reservation not found for property_id={self.reservations_seller.property_id}, buyer_id={buyer_id}.")
                return 404
            result = redis_client.set(f"property_id:{self.reservations_seller.property_id}:reservations_seller", json.dumps(new_data))
            logger.info(f"Seller reservation deleted for property_id={self.reservations_seller.property_id}, buyer_id={buyer_id}.")
            if not result:
                return 500
            return 200
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error deleting seller reservation: {e}")
            return 500
        
    def delete_reservations_seller_by_property_id_and_buyer_id(self) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            return 500
        raw_data = redis_client.get(f"property_id:{self.reservations_seller.property_id}:reservations_seller")
        if not raw_data:
            logger.warning(f"No seller reservations found for property_id={self.reservations_seller.property_id}.")
            return 404
        try:
            data = json.loads(raw_data)
            new_data = [res for res in data if res.get("buyer_id") != self.reservations_seller.reservations.buyer_id]
            if len(new_data) == len(data):
                logger.info(f"Seller reservation not found for property_id={self.reservations_seller.property_id}, buyer_id={buyer_id}.")
                return 404
            result = redis_client.set(f"property_id:{self.reservations_seller.property_id}:reservations_seller", json.dumps(new_data))
            logger.info(f"Seller reservation deleted for property_id={self.reservations_seller.property_id}, buyer_id={buyer_id}.")
            if not result:
                return 500
            return 200
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error deleting seller reservation: {e}")
            return 500

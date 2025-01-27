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
    
    # Flow of execution:
    # Done:
    # Si aggiunge una nuova casa in vendita -> nessun cambiamento (si risparmia spazio facendo in modo i record esistano solo se ci sono prenotazioni)
    # Si cambiano i dati di contatto di un utente -> si tollera che i dati siano vecchi, tanto sono dati volatili
    # Cliccato view reservation dal buyer -> mostra le sue prenotazioni (gestione del caso in cui non ci siano prenotazioni)
    # Cliccato view reservation dal seller -> mostra le prenotazioni per una sua casa (gestione del caso in cui non ci siano prenotazioni)
    # Si cancella una prenotazione -> va cancellata in reservationsseller e reservationsbuyer e diminuito attendees in openhouseevent
    
    # To do:
    # Arriva l'open house event -> il ttl di openhouseevent scade e si cancella, allo stesso modo si elimina la reservationsseller, mentre si aggiorna reservationbuyer, eliminando la specifica prenotazione
    # Book Now cliccato (nuova prenotazione in genere):
    # OpenHouseEvent non presente (prima reservation) -> creazione openhouseevent, reservationseller e inserimento prenotazione in reservationsbuyer
    # OpenHouseEvent presente (prenotazione successiva) -> aggiornamento reservationseller e reservationsbuyer e attendees in openhouseevent
    # Reservation gia presente -> la scrittura fallisce e si notifica l'utente che è già prenotato
    
    # To do (necessario Mongo):
    # Si aggiorna l'open house time -> va aggiornato openhouseevent e reservationsbuyer e possibilmente notificato l'utente
    # Si aggiorna thumbnail, prezzo, indirizzo -> va aggiornato reservationsbuyer
    # Si cancella una casa in vendita -> va cancellato openhouseevent e reservationsseller e cancellate le prenotazioni in reservationsbuyer
    # Si vende una casa -> va cancellato openhouseevent e reservationsseller e cancellate le prenotazioni in reservationsbuyer
    # Si cancella un'utente dalla piattaforma:
    #   Caso buyer: non si verifica mai (le aziende sono verificate)
    #   Caso seller: va cancellato reservationsseller, diminuito attendees in openhouseevent e cancellate le prenotazioni di quell'utente in reservationsbuyer
# oss: bisogna stare attenti all'atomicità delle operazioni
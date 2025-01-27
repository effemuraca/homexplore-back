
import json
from entities.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS
from setup.redis_setup.redis_setup import get_redis_client

class ReservationsSellerDB:
    reservations_seller: ReservationsSeller = None
    
    def __init__(self, reservations_seller: ReservationsSeller):
        self.reservations_seller = reservations_seller

    def get_reservations_seller_by_property_id(self, property_id: int) -> ReservationsSeller:
        if not property_id:
            return None
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:reservations")
        if not raw_data:
            return None
        data = json.loads(raw_data)
        reservation_list = []
        for item in data:
            reservation_list.append(
                ReservationS(
                    user_id=item.get("user_id"),
                    full_name=item.get("full_name"),
                    email=item.get("email"),
                    phone=item.get("phone")
                )
            )
        self.reservations_seller = ReservationsSeller(property_id=property_id, reservations=reservation_list)
        return self.reservations_seller

    def delete_reservations_seller_by_property_id(self, property_id: int) -> bool:
        if not property_id:
            return False
        redis_client = get_redis_client()
        result = redis_client.delete(f"property_id:{property_id}:reservations")
        return bool(result)

    def create_reservations_seller(self, property_id: int, reservation: ReservationS) -> bool:
        if not property_id or not reservation:
            return False
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:reservations")
        if not raw_data:
            data = []
        else:
            data = json.loads(raw_data)

        data.append({
            "user_id": reservation.user_id,
            "full_name": reservation.full_name,
            "email": reservation.email,
            "phone": reservation.phone
        })
        result = redis_client.set(f"property_id:{property_id}:reservations", json.dumps(data))
        return bool(result)

    def update_reservations_seller(self, property_id: int, reservation: ReservationS) -> bool:
        if not property_id or not reservation:
            return False
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:reservations")
        if not raw_data:
            return False
        data = json.loads(raw_data)
        if not data:
            return False

        # Aggiorna il primo match o l'intera lista a piacere
        item = data[0]
        if reservation.user_id is not None:
            item["user_id"] = reservation.user_id
        if reservation.full_name is not None:
            item["full_name"] = reservation.full_name
        if reservation.email is not None:
            item["email"] = reservation.email
        if reservation.phone is not None:
            item["phone"] = reservation.phone

        data[0] = item
        result = redis_client.set(f"property_id:{property_id}:reservations", json.dumps(data))
        return bool(result)
    
    def delete_reservations_seller_by_user_and_property(self, user_id: int, property_id: int) -> bool:
        if not user_id or not property_id:
            return False
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:reservations")
        if not raw_data:
            return False
        data = json.loads(raw_data)
        if not data:
            return False

        # Cancella il primo match
        for i, item in enumerate(data):
            if item["user_id"] == user_id:
                del data[i]
                break

        result = redis_client.set(f"property_id:{property_id}:reservations", json.dumps(data))
        return bool(result)
    
    def update_reservation_seller(self, property_id: int, reservation_id: int, reservation: ReservationS) -> bool:
        if not property_id or not reservation_id or not reservation:
            return False
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:reservations")
        if not raw_data:
            return False
        data = json.loads(raw_data)
        if not data:
            return False

        for item in data:
            if item.get("reservation_id") == reservation_id:
                # Update fields
                if reservation.user_id is not None:
                    item["user_id"] = reservation.user_id
                if reservation.full_name is not None:
                    item["full_name"] = reservation.full_name
                if reservation.email is not None:
                    item["email"] = reservation.email
                if reservation.phone is not None:
                    item["phone"] = reservation.phone
                break

        result = redis_client.set(f"property_id:{property_id}:reservations", json.dumps(data))
        return bool(result)
    
    # Flow of execution:
    # Done:
    # Si aggiunge una nuova casa in vendita -> nessun cambiamento (si risparmia spazio facendo in modo i record esistano solo se ci sono prenotazioni)
    # Si cambiano i dati di contatto di un utente -> si tollera che i dati siano vecchi, tanto sono dati volatili
    # Cliccato view reservation dal buyer -> mostra le sue prenotazioni (gestione del caso in cui non ci siano prenotazioni)
    # Cliccato view reservation dal seller -> mostra le prenotazioni per una sua casa (gestione del caso in cui non ci siano prenotazioni)
    
    # To do:
    # Si cancella una prenotazione -> va cancellata in reservationsseller e reservationsbuyer e diminuito attendees in openhouseevent
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
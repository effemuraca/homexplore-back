import json
from entities.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS
from setup.redis_setup.redis_setup import get_redis_client

class ReservationsSellerDB:
    reservations_seller:ReservationsSeller = None
    
    def __init__(self, reservations_seller:ReservationsSeller):
        self.reservations_seller = reservations_seller
        
    def get_reservations_seller_by_property_id(self, property_id:int) -> ReservationsSeller:
        if not property_id:
            return None
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:reservations")
        if not raw_data:
            return None
        data = json.loads(raw_data)
        reservations_list = []
        for item in data:
            reservations_list.append(
                ReservationS(
                    full_name=item["full_name"],
                    email=item["email"],
                    phone=item["phone"]
                )
            )
        self.reservations_seller = ReservationsSeller(property_id=property_id, reservations=reservations_list)
        return True

    def delete_reservations_seller_by_property_id(self, property_id: int) -> bool:
        if not property_id:
            return False
        redis_client = get_redis_client()
        result = redis_client.delete(f"property_id:{property_id}:reservations")
        return bool(result)
    
    def create_reservations_seller(self, property_id:int, expire_time:int, reservation:ReservationS) -> bool:
        if not property_id or not reservation:
            return False
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:reservations")
        if not raw_data:
            data = []
        else:
            data = json.loads(raw_data)
        data.append({
            "full_name": reservation.full_name,
            "email": reservation.email,
            "phone": reservation.phone
        })
        result = redis_client.set(f"property_id:{property_id}:reservations", json.dumps(data))
        redis_client.expire(f"property_id:{property_id}:reservations", expire_time)
        return bool(result)
    
    def update_reservations_seller(self, property_id:int = None, reservation:ReservationS = None) -> bool:
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:reservations")
        if not raw_data:
            return False
        data = json.loads(raw_data)
        for item in data:
            if reservation.full_name:
                item["full_name"] = reservation.full_name
            if reservation.email:
                item["email"] = reservation.email
            if reservation.phone:
                item["phone"] = reservation.phone
            break
        result = redis_client.set(f"property_id:{property_id}:reservations", json.dumps(data))
        return bool(result)
    
    # Flow of execution:
    # Done:
    # Si aggiunge una nuova casa in vendita -> nessun cambiamento (si risparmia spazio facendo in modo i record esistano solo se ci sono prenotazioni)
    # Si cambiano i dati di contatto di un utente -> si tollera che i dati siano vecchi, tanto sono dati volatili
    
    # To do:
    # Si cancella una prenotazione -> va cancellata in reservationsseller e reservationsbuyer e diminuito attendees in openhouseevent
    # Cliccato view reservation dal buyer -> mostra le sue prenotazioni (gestione del caso in cui non ci siano prenotazioni)
    # Cliccato view reservation dal seller -> mostra le prenotazioni per una sua casa (gestione del caso in cui non ci siano prenotazioni)
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
    
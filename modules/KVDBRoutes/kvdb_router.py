from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from setup.redis_setup.redis_setup import get_redis_client, WatchError
from setup.mongo_setup.mongo_setup import get_default_mongo_db
from modules.KVDBRoutes.models import response_models as ResponseModels
from modules.KVDBRoutes.models import kvdb_models as KVDBModels
from entities.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB
from entities.ReservationsBuyer.db_reservations_buyer import ReservationsBuyerDB
from entities.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS
from entities.ReservationsSeller.db_reservations_seller import ReservationsSellerDB
from entities.OpenHouseEvent.open_house_event import OpenHouseEvent, OpenHouseInfo
from entities.OpenHouseEvent.db_open_house_event import OpenHouseEventDB
from entities.Buyer.buyer import Buyer
from entities.Buyer.db_buyer import BuyerDB
import json
import logging
from bson.objectid import ObjectId

kvdb_router = APIRouter(prefix="/kvdb", tags=["kvdb"])

# Configure the logger
logger = logging.getLogger(__name__)

# Reservation deleted by buyer
@kvdb_router.delete(
    "/delete_reservation_by_user_and_property/{user_id}/{property_id}",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.ReservationDeletedResponses
)
def delete_reservation_by_user_and_property(user_id: str, property_id: str):
    """
    Delete a buyer reservation for a given user_id and property_id,
    decrement the open house attendees, and remove the seller reservation.
    This is done atomically using Redis transactions (WATCH/MULTI/EXEC).
    """
   
    open_house_ev = OpenHouseEvent(property_id=property_id)
    open_house_db = OpenHouseEventDB(open_house_ev)
    reservations_buyer = ReservationsBuyer(buyer_id=user_id)
    reservations_buyer_db = ReservationsBuyerDB(reservations_buyer)
    reservations_seller = ReservationsSeller(property_id=property_id)
    reservations_seller_db = ReservationsSellerDB(reservations_seller)


    redis_client = get_redis_client()
    if redis_client is None:
        raise HTTPException(status_code=500, detail="Failed to connect to Redis")

    try:
        # Start WATCH on all keys involved
        buyer_key = f"buyer_id:{user_id}:reservations"
        seller_key = f"property_id:{property_id}:reservations_seller"
        open_house_key = f"property_id:{property_id}:open_house_info"
        redis_client.watch(buyer_key, seller_key, open_house_key)


        # Perform deletions
        status = reservations_buyer_db.delete_reservation_by_property_id(property_id)
        if status == 404:
            redis_client.unwatch()
            raise HTTPException(status_code=404, detail="Reservation not found")
        if status == 500:
            redis_client.unwatch()
            raise HTTPException(status_code=500, detail="Error deleting reservation")

        status = reservations_seller_db.delete_reservation_seller_by_property_id_and_buyer_id(user_id)
        if status == 404:
            redis_client.unwatch()
            raise HTTPException(status_code=404, detail="Seller Reservation not found")
        if status == 500:
            redis_client.unwatch()
            raise HTTPException(status_code=500, detail="Error deleting seller reservation")

        status = open_house_db.decrement_attendees()
        if status == 404:
            redis_client.unwatch()
            raise HTTPException(status_code=404, detail="Open house event not found")
        if status == 500:
            redis_client.unwatch()
            raise HTTPException(status_code=500, detail="Error decrementing attendees")
        
        # Execute transaction
        with redis_client.pipeline() as pipe:
            try:
                pipe.multi()
                # Deletions have already been done via DB methods
                pipe.execute()
            except WatchError:
                logger.error("Transaction failed due to concurrent modification.")
                raise HTTPException(status_code=500, detail="Transaction failed")
        
        return JSONResponse(status_code=200, content={"detail": "Reservation deleted successfully"})
    
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred")


    


    # Done:
    # Si aggiunge una nuova casa in vendita -> nessun cambiamento (si risparmia spazio facendo in modo i record esistano solo se ci sono prenotazioni)
    # Si cambiano i dati di contatto di un utente -> si tollera che i dati siano vecchi, tanto sono dati volatili
    # Cliccato view reservation dal buyer -> mostra le sue prenotazioni (gestione del caso in cui non ci siano prenotazioni)
    # Cliccato view reservation dal seller -> mostra le prenotazioni per una sua casa (gestione del caso in cui non ci siano prenotazioni)
    # Si cancella una prenotazione -> va cancellata in reservationsseller e reservationsbuyer e diminuito attendees in openhouseevent
    # Book Now cliccato (nuova prenotazione in genere):
    # OpenHouseEvent non presente (prima reservation) -> creazione openhouseevent, reservationseller e inserimento prenotazione in reservationsbuyer
    # OpenHouseEvent presente (prenotazione successiva) -> aggiornamento reservationseller e reservationsbuyer e attendees in openhouseevent
    # Reservation gia presente -> la scrittura fallisce e si notifica l'utente che è già prenotato 
   

    # To do:
    # Arriva l'open house event -> il ttl di openhouseevent scade e si cancella, allo stesso modo si elimina la reservationsseller, mentre si aggiorna reservationbuyer, eliminando la specifica prenotazione
     # Si cancella un'utente dalla piattaforma:
    #   Caso seller: ...
    #   Caso buyer: va cancellato reservationsseller, diminuito attendees in openhouseevent e cancellate le prenotazioni di quell'utente in reservationsbuyer
    # Si aggiorna l'open house time -> va aggiornato openhouseevent e reservationsbuyer e possibilmente notificato l'utente (necessario PropertyOnSale)
    # Si aggiorna thumbnail, prezzo, indirizzo -> va aggiornato reservationsbuyer (necessario PropertyOnSale)
    # Si cancella una casa in vendita -> va cancellato openhouseevent e reservationsseller e cancellate le prenotazioni in reservationsbuyer (necessario PropertyOnSale)
    # Si vende una casa -> va cancellato openhouseevent e reservationsseller e cancellate le prenotazioni in reservationsbuyer (necessario PropertyOnSale)
# oss: bisogna stare attenti all'atomicità delle operazioni
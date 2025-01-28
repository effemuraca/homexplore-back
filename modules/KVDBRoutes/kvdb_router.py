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
    response_model=KVDBModels.SuccessModel,
    responses=ResponseModels.ReservationDeletedResponses
)
def delete_reservation_by_user_and_property(user_id: int, property_id: int):
    """
    Delete a buyer reservation for a given user_id and property_id,
    decrement the open house attendees, and remove the seller reservation.
    This is done atomically using Redis transactions (WATCH/MULTI/EXEC).
    """
    buyer_key = f"buyer_id:{user_id}:reservations"
    oh_key = f"property_id:{property_id}:open_house_info"
    seller_key = f"property_id:{property_id}:reservations_seller"
    redis = get_redis_client()

    with redis.pipeline() as pipe:
        while True:
            try:
                pipe.watch(buyer_key, oh_key, seller_key)

                buyer_data = pipe.get(buyer_key)
                oh_data = pipe.get(oh_key)
                seller_data = pipe.get(seller_key)

                # If any of the keys is missing, raise 404
                if not buyer_data:
                    logger.warning(f"Buyer reservation not found for user_id={user_id}, property_id={property_id}")
                    raise HTTPException(status_code=404, detail="Buyer reservation not found")
                if not oh_data:
                    logger.warning(f"Open house event not found for property_id={property_id}")
                    raise HTTPException(status_code=404, detail="Open house event not found")
                if not seller_data:
                    logger.warning(f"Seller reservation not found for user_id={user_id}, property_id={property_id}")
                    raise HTTPException(status_code=404, detail="Seller reservation not found")

                # Parse open house event data
                open_house_event = json.loads(oh_data)
                attendees = open_house_event.get("attendees", 0)

                if attendees <= 0:
                    logger.warning(f"No attendees left to decrement for property_id={property_id}")
                    raise HTTPException(status_code=404, detail="No attendees left to decrement")

                # Begin transaction
                pipe.multi()
                # Remove buyer reservation
                reservations = json.loads(buyer_data)
                updated_reservations = [res for res in reservations if res.get("property_id") != property_id]
                pipe.set(buyer_key, json.dumps(updated_reservations))
                # Decrement attendees
                open_house_event["attendees"] = attendees - 1
                pipe.set(oh_key, json.dumps(open_house_event))
                # Remove seller reservation
                seller_reservations = json.loads(seller_data)
                updated_seller_reservations = [res for res in seller_reservations if res.get("user_id") != user_id]
                pipe.set(seller_key, json.dumps(updated_seller_reservations))

                pipe.execute()
                break
            except WatchError:
                logger.error("WatchError occurred, data changed during transaction.")
                raise HTTPException(status_code=409, detail="Conflict: data changed, please retry.")
            except HTTPException as he:
                raise he
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise HTTPException(status_code=500, detail="Internal server error.")

    # If no exceptions, operation was successful
    logger.info(f"Reservation deleted successfully for user_id={user_id}, property_id={property_id}")
    return KVDBModels.SuccessModel(detail="Reservation deleted successfully")

@kvdb_router.post(
    "/book_now",
    response_model=KVDBModels.SuccessModel,
    responses=ResponseModels.BookNowResponses
)
def book_now(buyer_id: int, property_id: int, date: str, time: str, thumbnail: str, address: str):
    """
    Book an open house event for a given user_id and property_id,
    handling the case where the open house event is not present,
    the case where the open house event is present,
    and the case where the reservation is already present.
    This is done atomically using Redis transactions (WATCH/MULTI/EXEC).
    """
    buyer_key = f"buyer_id:{buyer_id}:reservations"
    oh_key = f"property_id:{property_id}:open_house_info"
    seller_key = f"property_id:{property_id}:reservations_seller"
    
    redis = get_redis_client()
    mongo_client = get_default_mongo_db()

    new_reservation = {
        "property_id": property_id,
        "date": date,
        "time": time,
        "thumbnail": thumbnail,
        "address": address
    }

    contact_info = mongo_client.buyers.find_one({"_id": ObjectId(buyer_id)})
    if not contact_info:
        logger.warning(f"Buyer not found for buyer_id={buyer_id}")
        raise HTTPException(status_code=404, detail="Buyer not found")
    
    # Create ReservationS object
    reservation = ReservationS(
        user_id=buyer_id,
        full_name=f"{contact_info.get('name', '')} {contact_info.get('surname', '')}",
        email=contact_info.get('email', ''),
        phone=contact_info.get('phone_number', '')
    )

    with redis.pipeline() as pipe:
        while True:
            try:
                pipe.watch(buyer_key, oh_key, seller_key)

                buyer_data = pipe.get(buyer_key)
                oh_data = pipe.get(oh_key)
                seller_data = pipe.get(seller_key)

                # Initialize reservations list if buyer_data is None
                if buyer_data:
                    buyer_reservations = json.loads(buyer_data)
                    # Check if reservation already exists
                    if any(res.get("property_id") == property_id for res in buyer_reservations):
                        logger.warning(f"Reservation already exists for buyer_id={buyer_id}, property_id={property_id}")
                        raise HTTPException(status_code=400, detail="Reservation already exists")
                else:
                    buyer_reservations = []

                # Begin transaction
                pipe.multi()

                if not oh_data:
                    # OpenHouseEvent not present (first reservation)
                    open_house_info = OpenHouseInfo(date=date, time=time, max_attendees=50, attendees=1)
                    open_house_event = OpenHouseEvent(property_id=property_id, open_house_info=open_house_info)
                    pipe.set(oh_key, open_house_event.model_dump_json())

                    # Create ReservationsSeller
                    reservations_seller = reservation
                    pipe.set(seller_key, reservations_seller.model_dump_json())

                    # Insert reservation in ReservationsBuyer
                    buyer_reservations.append(new_reservation)
                    pipe.set(buyer_key, json.dumps(buyer_reservations))
                else:
                    # OpenHouseEvent present (subsequent reservations)
                    open_house_event = json.loads(oh_data)
                    max_attendees = open_house_event.get("max_attendees", 50)
                    attendees = open_house_event.get("attendees", 0)

                    if attendees >= max_attendees:
                        logger.warning(f"Attendees limit reached for property_id={property_id}")
                        raise HTTPException(status_code=400, detail="Attendees limit reached")

                    
                    # Update ReservationsSeller
                    if seller_data:
                        reservations_seller = json.loads(seller_data)
                        # Check if seller reservation exists
                        if not any(res.get("user_id") == buyer_id for res in reservations_seller):
                            reservations_seller.append(reservation)
                            pipe.set(seller_key, json.dumps(reservations_seller))
                    else:
                        # If seller reservations do not exist, create them
                        reservations_seller = [reservation]
                        pipe.set(seller_key, json.dumps(reservations_seller))

                    # Update ReservationsBuyer
                    buyer_reservations.append(new_reservation)
                    pipe.set(buyer_key, json.dumps(buyer_reservations))

                    # Increment attendees
                    open_house_event["attendees"] = attendees + 1
                    pipe.set(oh_key, json.dumps(open_house_event))

                pipe.execute()
                break
            except WatchError:
                logger.error("WatchError occurred, data changed during transaction.")
                raise HTTPException(status_code=409, detail="Conflict: data changed, please retry.")
            except HTTPException as he:
                raise he
            except Exception as e:
                logger.error(f"Unexpected error during booking: {e}")
                raise HTTPException(status_code=500, detail="Internal server error.")

    # If no exceptions, operation was successful
    logger.info(f"Reservation created successfully for user_id={buyer_id}, property_id={property_id}")
    return KVDBModels.SuccessModel(detail="Reservation created successfully")

@kvdb_router.delete(
    "/delete_user/{user_id}",
    response_model=KVDBModels.SuccessModel,
    responses=ResponseModels.DeleteUserResponses
)
def delete_user(user_id: int):
    """
    Delete a user by user_id, removing all their reservations and updating the open house events.
    This is done atomically using Redis transactions (WATCH/MULTI/EXEC).
    """
    buyer_key = f"buyer_id:{user_id}:reservations"
    redis = get_redis_client()
    mongo_client = get_default_mongo_db()

    result = mongo_client.buyers.delete_one({"_id": ObjectId(user_id)})
    if not result.deleted_count:
        logger.warning(f"Buyer not found for user_id={user_id}")
        raise HTTPException(status_code=404, detail="Buyer not found")

    with redis.pipeline() as pipe:
        while True:
            try:
                pipe.watch(buyer_key)
                reservationsbuyer_data = pipe.get(buyer_key)

                if not reservationsbuyer_data:
                    logger.warning(f"No reservations found for user_id={user_id}")
                    raise HTTPException(status_code=404, detail="No reservations found for user.")

                # Begin transaction
                pipe.multi()
                # Delete reservationsbuyer
                pipe.delete(buyer_key)

                # Fetch all reservations to update reservationsseller and openhouseevent
                reservationsbuyer = json.loads(reservationsbuyer_data)
                for reservation in reservationsbuyer:
                    property_id = reservation.get("property_id")
                    oh_key = f"property_id:{property_id}:open_house_info"
                    seller_key = f"property_id:{property_id}:reservations_seller"

                    # Decrement attendees in openhouseevent
                    oh_data = pipe.get(oh_key)
                    if oh_data:
                        open_house_event = json.loads(oh_data)
                        open_house_event["attendees"] -= 1
                        pipe.set(oh_key, json.dumps(open_house_event))

                    # Delete reservation from reservationsseller
                    seller_data = pipe.get(seller_key)
                    if seller_data:
                        seller_reservations = json.loads(seller_data)
                        updated_seller_reservations = [
                            res for res in seller_reservations if res.get("user_id") != user_id
                        ]
                        pipe.set(seller_key, json.dumps(updated_seller_reservations))

                pipe.execute()
                break
            except WatchError:
                logger.error("WatchError occurred, data changed during transaction.")
                raise HTTPException(status_code=409, detail="Conflict: data changed, please retry.")
            except HTTPException as he:
                raise he
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise HTTPException(status_code=500, detail="Internal server error.")

    # If no exceptions, operation was successful
    logger.info(f"User deleted successfully for user_id={user_id}")
    return KVDBModels.SuccessModel(detail="User deleted successfully")

    # Done:
    # Si aggiunge una nuova casa in vendita -> nessun cambiamento (si risparmia spazio facendo in modo i record esistano solo se ci sono prenotazioni)
    # Si cambiano i dati di contatto di un utente -> si tollera che i dati siano vecchi, tanto sono dati volatili
    # Cliccato view reservation dal buyer -> mostra le sue prenotazioni (gestione del caso in cui non ci siano prenotazioni)
    # Cliccato view reservation dal seller -> mostra le prenotazioni per una sua casa (gestione del caso in cui non ci siano prenotazioni)
    # Si cancella una prenotazione -> va cancellata in reservationsseller e reservationsbuyer e diminuito attendees in openhouseevent
    
    # Done (anche Mongo):
    # Book Now cliccato (nuova prenotazione in genere):
    # OpenHouseEvent non presente (prima reservation) -> creazione openhouseevent, reservationseller e inserimento prenotazione in reservationsbuyer
    # OpenHouseEvent presente (prenotazione successiva) -> aggiornamento reservationseller e reservationsbuyer e attendees in openhouseevent
    # Reservation gia presente -> la scrittura fallisce e si notifica l'utente che è già prenotato 
    # Si cancella un'utente dalla piattaforma:
    #   Caso seller: non si verifica mai (le aziende sono verificate)
    #   Caso buyer: va cancellato reservationsseller, diminuito attendees in openhouseevent e cancellate le prenotazioni di quell'utente in reservationsbuyer


    # To do:
    # Arriva l'open house event -> il ttl di openhouseevent scade e si cancella, allo stesso modo si elimina la reservationsseller, mentre si aggiorna reservationbuyer, eliminando la specifica prenotazione
  
    # To do (necessario Mongo):
    # Si aggiorna l'open house time -> va aggiornato openhouseevent e reservationsbuyer e possibilmente notificato l'utente (necessario PropertyOnSale)
    # Si aggiorna thumbnail, prezzo, indirizzo -> va aggiornato reservationsbuyer (necessario PropertyOnSale)
    # Si cancella una casa in vendita -> va cancellato openhouseevent e reservationsseller e cancellate le prenotazioni in reservationsbuyer (necessario PropertyOnSale)
    # Si vende una casa -> va cancellato openhouseevent e reservationsseller e cancellate le prenotazioni in reservationsbuyer (necessario PropertyOnSale)
# oss: bisogna stare attenti all'atomicità delle operazioni
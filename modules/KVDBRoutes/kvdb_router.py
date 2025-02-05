from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from setup.redis_setup.redis_setup import get_redis_client, WatchError
from setup.mongo_setup.mongo_setup import get_mongo_client
from modules.KVDBRoutes.models import response_models as ResponseModels
from modules.KVDBRoutes.models.kvdb_models import BookNow
from entities.Redis.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB
from entities.Redis.ReservationsBuyer.db_reservations_buyer import ReservationsBuyerDB
from entities.Redis.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS, next_weekday
from entities.Redis.ReservationsSeller.db_reservations_seller import ReservationsSellerDB
from entities.MongoDB.Buyer.buyer import Buyer
from entities.MongoDB.Buyer.db_buyer import BuyerDB
from bson.objectid import ObjectId
from datetime import datetime
import logging

kvdb_router = APIRouter(prefix="/kvdb", tags=["kvdb"])

# Configure the logger
logger = logging.getLogger(__name__)

# Reservation deleted by buyer
@kvdb_router.delete(
    "/delete_reservation_by_user_and_property/{user_id}/{property_on_sale_id}",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.ReservationDeletedResponses
)
def delete_reservation_by_user_and_property(user_id: str, property_on_sale_id: str):
    """
    Delete a buyer reservation for a given user_id and property_on_sale_id and remove the seller reservation.
    This is done atomically using Redis transactions (WATCH/MULTI/EXEC).
    """
   
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user_id")
    if not ObjectId.is_valid(property_on_sale_id):
        raise HTTPException(status_code=400, detail="Invalid property_on_sale_id")
                            
    reservations_buyer = ReservationsBuyer(buyer_id=user_id)
    reservations_buyer_db = ReservationsBuyerDB(reservations_buyer)
    reservations_seller = ReservationsSeller(property_on_sale_id=property_on_sale_id)
    reservations_seller_db = ReservationsSellerDB(reservations_seller)


    redis_client = get_redis_client()
    if redis_client is None:
        raise HTTPException(status_code=500, detail="Failed to connect to Redis")

    try:
        # Start WATCH on all keys involved
        buyer_key = f"buyer_id:{user_id}:reservations"
        seller_key = f"property_on_sale_id:{property_on_sale_id}:reservations_seller"
        redis_client.watch(buyer_key, seller_key)


        # Perform deletions
        status = reservations_buyer_db.delete_reservation_by_property_on_sale_id(property_on_sale_id)
        if status == 404:
            redis_client.unwatch()
            raise HTTPException(status_code=404, detail="Reservation not found")
        if status == 500:
            redis_client.unwatch()
            raise HTTPException(status_code=500, detail="Error deleting reservation")

        status = reservations_seller_db.delete_reservation_seller_by_buyer_id(user_id)
        if status == 404:
            redis_client.unwatch()
            raise HTTPException(status_code=404, detail="Seller Reservation not found")
        if status == 500:
            redis_client.unwatch()
            raise HTTPException(status_code=500, detail="Error deleting seller reservation")

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


@kvdb_router.post(
    "/book_now",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.BookNowResponses
)
def book_now(book_now_info: BookNow):
    """
    Book an open house event for a given buyer_id and property_on_sale_id,
    handling the case where the open house event is not present (first reservation),
    the case where the open house event is present (subsequent reservation),
    and the case where the reservation is already present.
    """

    buyer = Buyer(buyer_id=book_now_info.buyer_id)
    buyer_db = BuyerDB(buyer)
    
    status = buyer_db.get_contact_info(book_now_info.buyer_id)
    if status == 404:
        raise HTTPException(status_code=404, detail="Buyer not found")
    if status == 500:
        raise HTTPException(status_code=500, detail="Error decoding buyer data")

    buyer = buyer_db.buyer
    if not all([buyer.name, buyer.surname, buyer.email, buyer.phone_number]):
        logger.error("Incomplete buyer data for booking")
        raise HTTPException(status_code=500, detail="Incomplete buyer data")

    reservations_buyer = ReservationsBuyer(buyer_id=book_now_info.buyer_id)
    reservations_buyer_db = ReservationsBuyerDB(reservations_buyer)
    reservations_seller = ReservationsSeller(property_on_sale_id=book_now_info.property_on_sale_id)
    reservations_seller_db = ReservationsSellerDB(reservations_seller)

        
    status = reservations_buyer_db.get_reservations_by_user()
    if status == 500:
        raise HTTPException(status_code=500, detail="Error decoding reservations data")
    if status == 200:
        raise HTTPException(status_code=400, detail="Buyer already has a reservation")
    
    status = reservations_seller_db.get_reservation_seller()
    if status == 500:
        raise HTTPException(status_code=500, detail="Error decoding seller reservations data")
    
    new_reservation = ReservationS(
        buyer_id=book_now_info.buyer_id, 
        full_name=f"{buyer.name} {buyer.surname}",
        email=buyer.email,
        phone=buyer.phone_number
    )
    
    if reservations_seller_db.reservations_seller.reservations is None:
        reservations_seller_db.reservations_seller.reservations = []
    reservations_seller_db.reservations_seller.reservations.append(new_reservation)

    status = reservations_seller_db.create_reservation_seller(book_now_info.day, book_now_info.time, book_now_info.buyer_id, book_now_info.max_reservations)
    if status == 500:
        raise HTTPException(status_code=500, detail="Error creating seller reservation")
    if status == 409:
        raise HTTPException(status_code=409, detail="Reservation already exists")
    
    date = next_weekday(book_now_info.day)

    reservations_buyer_db.reservations_buyer.reservations = [
        ReservationB(
            property_on_sale_id = book_now_info.property_on_sale_id, 
            date = date, 
            time = book_now_info.time, 
            thumbnail = book_now_info.thumbnail, 
            address = book_now_info.address
        )
    ]
    status = reservations_buyer_db.create_reservation_buyer()
    if status == 500:
        raise HTTPException(status_code=500, detail="Error creating buyer reservation")
    
    return JSONResponse(status_code=200, content={"detail": "Reservation created successfully"})
            
@kvdb_router.get(
    "/get_reservations_by_buyer/{buyer_id}",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.GetReservationsResponses
)
def get_reservations_by_buyer(buyer_id: str):
    """
    Get reservations for a given buyer_id, 
    before showing the buyer the reservations,
    check if some of them are expired and delete them.
    """

    if not ObjectId.is_valid(buyer_id):
        raise HTTPException(status_code=400, detail="Invalid buyer_id")

    reservations_buyer = ReservationsBuyer(buyer_id=buyer_id)
    reservations_buyer_db = ReservationsBuyerDB(reservations_buyer)

    redis = get_redis_client()
    if redis is None:
        raise HTTPException(status_code=500, detail="Failed to connect to Redis.")
    
    try:
        with redis.pipeline() as pipe:
            while True:
                try:
                    pipe.watch(f"buyer_id:{buyer_id}:reservations")
                    existing = pipe.get(f"buyer_id:{buyer_id}:reservations")
                    if existing:
                        data = json.loads(existing)
                        reservations_buyer = ReservationsBuyer(**data)
                    else:
                        reservations_buyer = ReservationsBuyer(buyer_id=buyer_id, reservations=[])
                    pipe.multi()
                    pipe.execute()
                    break
                except WatchError:
                    continue
    except Exception as e:
        logger.error(f"Error decoding reservations data: {e}")
        raise HTTPException(status_code=500, detail="Error decoding reservations data.")
    
    status = reservations_buyer_db.get_reservations_by_user()
    if status == 404:
        raise HTTPException(status_code=404, detail="No reservations found for buyer.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Error decoding reservations data.")
    
    for res in reservations_buyer.reservations:
        if res.check_reservation_expired():
            status = reservations_buyer_db.delete_reservation_by_property_on_sale_id(res.property_on_sale_id)
            if status == 404:
                raise HTTPException(status_code=404, detail="Reservation not found")
            if status == 500:
                raise HTTPException(status_code=500, detail="Error deleting reservation")
            
    return reservations_buyer.reservations.json()


    # Done:
    # Si aggiunge una nuova casa in vendita -> nessun cambiamento (si risparmia spazio facendo in modo i record esistano solo se ci sono prenotazioni)
    # Si cambiano i dati di contatto di un utente -> si tollera che i dati siano vecchi, tanto sono dati volatili
    # Cliccato view reservation dal buyer -> mostra le sue prenotazioni (gestione del caso in cui non ci siano prenotazioni)
    # Cliccato view reservation dal seller -> mostra le prenotazioni per una sua casa (gestione del caso in cui non ci siano prenotazioni)
    # Si cancella una prenotazione -> va cancellata in reservationsseller e reservationsbuyer
    # Book Now cliccato (nuova prenotazione in genere):
    # ReservationSeller non presente (prima reservation) -> creazione reservationseller e inserimento prenotazione in reservationsbuyer
    # ReservationSeller presente (prenotazione successiva) -> aggiornamento reservationseller e reservationsbuyer 
    # Reservation gia presente -> la scrittura fallisce e si notifica l'utente che è già prenotato 
    # Arriva l'open house event -> il ttl di reservationsseller scade e si cancella, reservationsbuyer viene aggiornato quando il buyer clicca view reservation

    # To do:
    
    # Sistemare sulle route Mongo:
    # Si aggiorna l'open house time -> va aggiornato openhouseevent e reservationsbuyer e possibilmente notificato l'utente (necessario PropertyOnSale)
    # Si aggiorna thumbnail, prezzo, indirizzo -> va aggiornato reservationsbuyer (necessario PropertyOnSale)
    # Si cancella una casa in vendita -> va cancellato openhouseevent e reservationsseller e cancellate le prenotazioni in reservationsbuyer (necessario PropertyOnSale)
    # Si vende una casa -> va cancellato openhouseevent e reservationsseller e cancellate le prenotazioni in reservationsbuyer (necessario PropertyOnSale)
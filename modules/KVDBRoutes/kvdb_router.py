from fastapi import APIRouter, HTTPException, Depends
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
from modules.Auth.helpers.auth_helpers import JWTHandler, hash_password
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
def delete_reservation_by_buyer_and_property(property_on_sale_id: str, access_token: str = Depends(JWTHandler())):
    """
    Delete a buyer reservation for a given buyer_id and 
    property_on_sale_id and remove the seller reservation.
    """
    try:
        buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
        if not ObjectId.is_valid(property_on_sale_id):
            raise HTTPException(status_code=400, detail="Invalid property_on_sale_id")

        reservations_buyer = ReservationsBuyer(buyer_id=buyer_id)
        reservations_buyer_db = ReservationsBuyerDB(reservations_buyer)
        reservations_seller = ReservationsSeller(property_on_sale_id=property_on_sale_id)
        reservations_seller_db = ReservationsSellerDB(reservations_seller)

        status = reservations_buyer_db.get_reservations_by_user()
        if status == 500:
            raise HTTPException(status_code=500, detail="Error decoding buyer reservations data")
        if status == 404:
            raise HTTPException(status_code=404, detail="No reservations found for buyer")

        status = reservations_seller_db.get_reservation_seller()
        if status == 500:
            raise HTTPException(status_code=500, detail="Error decoding seller reservations data")
        if status == 404:
            raise HTTPException(status_code=404, detail="No reservations found for seller")

        # Check if the buyer has a reservation for the given property
        buyer_reservations = reservations_buyer_db.reservations_buyer.reservations
        if not buyer_reservations:
            raise HTTPException(status_code=404, detail="No reservations found for buyer")
        buyer_reservations = [res for res in buyer_reservations if res.property_on_sale_id == property_on_sale_id]
        if not buyer_reservations:
            raise HTTPException(status_code=404, detail="No reservations found for buyer")
        
        # Check if the seller has a reservation for the given buyer
        seller_reservations = reservations_seller_db.reservations_seller.reservations
        if not seller_reservations:
            raise HTTPException(status_code=404, detail="No reservations found for seller")
        seller_reservations = [res for res in seller_reservations if res.buyer_id == buyer_id]
        if not seller_reservations:
            raise HTTPException(status_code=404, detail="No reservations found for seller")
        
        # Delete the buyer reservation
        status = reservations_buyer_db.delete_reservation_by_property_on_sale_id(property_on_sale_id)
        if status == 500:
            raise HTTPException(status_code=500, detail="Error deleting buyer reservation")
        if status == 404:
            raise HTTPException(status_code=404, detail="No reservations found for buyer")
        
        # Delete the seller reservation
        status = reservations_seller_db.delete_reservation_seller_by_buyer_id(buyer_id)
        if status == 500:
            raise HTTPException(status_code=500, detail="Error deleting seller reservation")
        if status == 404:
            raise HTTPException(status_code=404, detail="No reservations found for seller")
        
        return JSONResponse(status_code=200, content={"detail": "Reservation deleted successfully"})
    
    except Exception as e:
        logger.error(f"Unhandled error in delete_reservation_by_buyer_and_property: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@kvdb_router.post(
    "/book_now",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.BookNowResponses
)
def book_now(book_now_info: BookNow, access_token: str = Depends(JWTHandler())):
    try:
        buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
        buyer = Buyer(buyer_id=buyer_id)
        buyer_db = BuyerDB(buyer)
        
        status = buyer_db.get_contact_info(buyer_id)
        if status == 404:
            raise HTTPException(status_code=404, detail="Buyer not found")
        if status == 500:
            raise HTTPException(status_code=500, detail="Error decoding buyer data")

        buyer = buyer_db.buyer
        if not all([buyer.name, buyer.surname, buyer.email, buyer.phone_number]):
            logger.error("Incomplete buyer data for booking")
            raise HTTPException(status_code=500, detail="Incomplete buyer data")

        reservations_buyer = ReservationsBuyer(buyer_id=buyer_id)
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
            buyer_id=buyer_id, 
            full_name=f"{buyer.name} {buyer.surname}",
            email=buyer.email,
            phone=buyer.phone_number
        )

        if reservations_seller_db.reservations_seller.reservations is None:
            reservations_seller_db.reservations_seller.reservations = []
        reservations_seller_db.reservations_seller.reservations.append(new_reservation)

        status = reservations_seller_db.create_reservation_seller(
                    book_now_info.day,
                    book_now_info.time,
                    buyer_id,
                    book_now_info.max_reservations
                )
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
    except Exception as e:
        logger.error(f"Unhandled error in book_now: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")           
@kvdb_router.get(
    "/get_reservations_by_buyer/{buyer_id}",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.GetReservationsResponses
)
def get_reservations_by_buyer(access_token: str = Depends(JWTHandler())):
    """
    Get reservations for a given buyer_id, 
    before showing the buyer the reservations,
    check if some of them are expired and delete them.
    """
    try:
        buyer_id, user_type = JWTHandler.verifyAccessToken(access_token)
        reservations_buyer = ReservationsBuyer(buyer_id=buyer_id)
        reservations_buyer_db = ReservationsBuyerDB(reservations_buyer)
        status = reservations_buyer_db.update_expired_reservations()
        if status == 500:
            raise HTTPException(status_code=500, detail="Error updating expired reservations")
        if status == 404:
            raise HTTPException(status_code=404, detail="No reservations found for buyer")
        return reservations_buyer_db.reservations_buyer.model_dump()
    
    except Exception as e:
        logger.error(f"Unhandled error in get_reservations_by_buyer: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")




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
import json
from typing import Optional
from bson.objectid import ObjectId
from entities.Buyer.buyer import Buyer  
from setup.mongo_setup.mongo_setup import get_default_mongo_db
import logging

# Configura il logger
logger = logging.getLogger(__name__)

class BuyerDB:
    def __init__(self, buyer: Optional[Buyer] = None):
        self.buyer = buyer

    def get_buyer_by_id(self, buyer_id: str) -> Optional[Buyer]:
        if not buyer_id:
            logger.error("buyer_id non fornito.")
            return 400
        mongo_client = get_default_mongo_db()
        data = mongo_client.buyers.find_one({"_id": ObjectId(buyer_id)})
        if not data:
            logger.warning(f"Buyer con id {buyer_id} non trovato.")
            return 404
        self.buyer = Buyer(
            buyer_id=str(data["_id"]),
            password=data["password"],
            email=data["email"],
            phone_number=data["phone_number"],
            name=data["name"],
            surname=data["surname"],
            age=data["age"]
        )
        logger.debug(f"Buyer recuperato: {self.buyer}")
        return 200

    def delete_buyer_by_id(self, buyer_id: str) -> bool:
        if not buyer_id:
            logger.error("buyer_id non fornito per la cancellazione.")
            return 400
        mongo_client = get_default_mongo_db()
        result = mongo_client.buyers.delete_one({"_id": ObjectId(buyer_id)})
        if result.deleted_count:
            logger.info(f"Buyer con id {buyer_id} cancellato con successo.")
            return 200
        else:
            logger.info(f"Buyer con id {buyer_id} non trovato.")
            return 404

    def create_buyer(self) -> bool:
        if not self.buyer:
            logger.error("Nessun buyer da creare.")
            return 400
        mongo_client = get_default_mongo_db()
        buyer_data = self.buyer.model_dump(exclude_none=True, exclude={"buyer_id"})
        result = mongo_client.buyers.insert_one(buyer_data)
        if result.inserted_id:
            self.buyer.buyer_id = str(result.inserted_id)
            logger.info(f"Buyer creato con id {self.buyer.buyer_id}.")
            return 200
        logger.error("Creazione del buyer fallita.")
        return 500

    def update_buyer(self, buyer: Buyer) -> bool:
        if not self.buyer or not self.buyer.buyer_id:
            logger.error("Buyer non inizializzato o buyer_id mancante per l'aggiornamento.")
            return 400
        mongo_client = get_default_mongo_db()
        update_data = buyer.model_dump(exclude_none=True, exclude={"buyer_id"})
        result = mongo_client.buyers.update_one(
            {"_id": ObjectId(self.buyer.buyer_id)},
            {"$set": update_data}
        )
        if result.modified_count:
            logger.info(f"Buyer aggiornato con buyer_id={self.buyer.buyer_id}.")
            return 200
        logger.warning(f"Nessuna modifica effettuata per buyer_id={self.buyer.buyer_id}.")
        return 500
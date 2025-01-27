from typing import Optional
from bson.objectid import ObjectId
from entities.Buyer.buyer import Buyer, BuyerInfo
from setup.mongo_setup.mongo_setup import get_default_mongo_db
import logging
import json

# Configura il logger
logger = logging.getLogger(__name__)

class BuyerDB:
    def __init__(self, buyer: Optional[Buyer] = None):
        self.buyer = buyer

    def get_buyer_by_id(self, buyer_id: str) -> Optional[Buyer]:
        if not buyer_id:
            logger.warning("Buyer ID non fornito per il recupero.")
            return None
        mongo_client = get_default_mongo_db()
        data = mongo_client.buyers.find_one({"_id": ObjectId(buyer_id)})
        if not data:
            logger.info(f"Buyer non trovato per buyer_id={buyer_id}.")
            return None
        self.buyer = Buyer(
            buyer_id=str(data["_id"]),
            password=data["password"],
            email=data["email"],
            phone_number=data["phone_number"],
            name=data["name"],
            surname=data["surname"],
            age=data.get("age")
        )
        logger.debug(f"Buyer recuperato: {self.buyer}")
        return self.buyer

    def delete_buyer_by_id(self, buyer_id: str) -> bool:
        if not buyer_id:
            logger.warning("Buyer ID non fornito per la cancellazione.")
            return False
        mongo_client = get_default_mongo_db()
        result = mongo_client.buyers.delete_one({"_id": ObjectId(buyer_id)})
        if result.deleted_count:
            logger.info(f"Buyer cancellato con buyer_id={buyer_id}.")
            return True
        logger.warning(f"Nessun buyer trovato da cancellare per buyer_id={buyer_id}.")
        return False

    def create_buyer(self) -> bool:
        if not self.buyer:
            logger.warning("Buyer non fornito per la creazione.")
            return False
        if not self.buyer.get_buyer_info():
            logger.warning("Informazioni incomplete del buyer per la creazione.")
            return False
        mongo_client = get_default_mongo_db()
        result = mongo_client.buyers.insert_one(self.buyer.get_buyer_info())
        if result.inserted_id:
            self.buyer.buyer_id = str(result.inserted_id)
            logger.info(f"Buyer creato con buyer_id={self.buyer.buyer_id}.")
            return True
        logger.error("Errore durante la creazione del buyer.")
        return False

    def update_buyer(self, buyer_info: BuyerInfo) -> bool:
        if not self.buyer or not self.buyer.buyer_id:
            logger.warning("Buyer non inizializzato o buyer_id mancante per l'aggiornamento.")
            return False
        if not buyer_info.is_valid():
            logger.warning("BuyerInfo non valido per l'aggiornamento.")
            return False
        mongo_client = get_default_mongo_db()
        update_data = buyer_info.dict(exclude_unset=True)
        if not update_data:
            logger.warning("Nessun dato da aggiornare.")
            return False
        result = mongo_client.buyers.update_one(
            {"_id": ObjectId(self.buyer.buyer_id)},
            {"$set": update_data}
        )
        if result.modified_count:
            logger.info(f"Buyer aggiornato con buyer_id={self.buyer.buyer_id}.")
            self.buyer.update_info(buyer_info)
            return True
        logger.warning(f"Nessuna modifica effettuata per buyer_id={self.buyer.buyer_id}.")
        return False
import json
from typing import Optional
from bson.objectid import ObjectId
from entities.MongoDB.Buyer.buyer import Buyer, FavouriteProperty
from setup.mongo_setup.mongo_setup import get_default_mongo_db
import logging

# Configura il logger
logger = logging.getLogger(__name__)

class BuyerDB:
    def __init__(self, buyer: Optional[Buyer] = None):
        self.buyer = buyer
    
    # buyer route (get buyer) #CONSISTENT

    def get_profile_info(self) -> int:
        if not self.buyer or not self.buyer.buyer_id:
            logger.error("Buyer info not initialized.")
            return 400
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return 500
        try:
            data = mongo_client.buyers.find_one({"_id": ObjectId(self.buyer.buyer_id)}, {"favourites": 0})
        except Exception as e:
            logger.exception("Error retrieving buyer profile: %s", e)
            return 500
        if not data:
            logger.warning(f"Buyer with id {self.buyer.buyer_id} not found.")
            return 404
        data["buyer_id"] = str(data.pop("_id"))
        self.buyer = Buyer(**data)
        return 200
    
    # buyer route (update buyer) #CONSISTENT
    def get_buyer_by_email(self, email: str) -> int:
        if not email:
            logger.error("Email not given.")
            return 400
        mongo_client = get_default_mongo_db()
        try:
            data = mongo_client.buyers.find_one({"email": email}, {"favourites": 0})
        except Exception as e:
            logger.exception("Error retrieving buyer by email: %s", e)
            return 500
        if not data:
            logger.warning(f"Buyer with email {email} not found.")
            return 404
        self.buyer = Buyer(
            buyer_id=str(data["_id"]),
            password=data["password"],
            email=data["email"],
            phone_number=data["phone_number"],
            name=data["name"],
            surname=data["surname"]
        )
        logger.debug(f"Buyer retrieved: {self.buyer}")
        return 200

    def delete_buyer_by_id(self, buyer_id: str) -> int:
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

    def create_buyer(self) -> int:
        if not self.buyer:
            logger.error("Nessun buyer da creare.")
            return 400
        mongo_client = get_default_mongo_db()
        buyer_data = self.buyer.model_dump(exclude_none=True, exclude={"buyer_id"})
        buyer_data["favourites"] = []
        result = mongo_client.buyers.insert_one(buyer_data)
        if result.inserted_id:
            self.buyer.buyer_id = str(result.inserted_id)
            logger.info(f"Buyer creato con id {self.buyer.buyer_id}.")
            return 201
        logger.error("Creazione del buyer fallita.")
        return 500
    
    # buyer route (update buyer) #CONSISTENT
    def update_buyer(self, buyer: Buyer) -> int:
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
    
    # buyer route (get favourites) #CONSISTENT
    def get_favourites(self) -> int:
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return 500
        try:
            data = mongo_client.buyers.find_one({"_id": ObjectId(self.buyer.buyer_id)}, {"favourites": 1})
        except Exception as e:
            logger.exception("Error retrieving favourites for buyer_id=%s: %s", self.buyer.buyer_id, e)
            return 500
        if not data or "favourites" not in data:
            logger.warning(f"Favourites non trovati per buyer_id={self.buyer.buyer_id}.")
            return 404
        self.buyer.favourites = [
            FavouriteProperty(
            **{"_id": str(fav["property_id"]),
               **{k: v for k, v in fav.items() if k != "property_id"}}
            )
            for fav in data.get("favourites", [])
        ]
        return 200
    
    # buyer route (add favourite) #CONSISTENT
    def add_favourite(self, buyer_id: str, favourite: FavouriteProperty) -> int:
        if not buyer_id:
            logger.error("buyer_id non fornito.")
            return 400
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return 500
        
        data={"_id": ObjectId(favourite.property_id), **favourite.model_dump(exclude={"property_id"})}
        try:
            result = mongo_client.buyers.update_one(
            {"_id": ObjectId(buyer_id)},
            {"$push": {"favourites": data}}
            )
        except Exception as e:
            logger.exception("Error adding favourite for buyer_id=%s: %s", buyer_id, e)
            return 500
        if result.modified_count:
            logger.info(f"Favourite aggiunto per buyer_id={buyer_id}.")
            return 200
        logger.warning(f"Favourite non aggiunto per buyer_id={buyer_id}.")
        return 500
    
    # buyer route (delete favourite) #CONSISTENT
    def delete_favourite(self, buyer_id: str, property_id: str) -> int:
        if not buyer_id or not property_id:
            logger.error("buyer_id o property_id non fornito.")
            return 400
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return 500
        result = mongo_client.buyers.update_one(
            {"_id": ObjectId(buyer_id)},
            {"$pull": {"favourites": {"_id": ObjectId(property_id)}}}
        )
        if result.modified_count:
            logger.info(f"Favourite rimosso per buyer_id={buyer_id}.")
            return 200
        logger.warning(f"Favourite non rimosso per buyer_id={buyer_id}.")
        return 500

    def update_favourite(self, buyer_id: str, property_id: str, updated_data: dict) -> int:
        if not buyer_id or not property_id:
            logger.error("buyer_id o property_id non fornito.")
            return 400
        mongo_client = get_default_mongo_db()
        result = mongo_client.buyers.update_one(
            {"_id": ObjectId(buyer_id), "favourites.property_id": property_id},
            {"$set": {"favourites.$": updated_data}}
        )
        if result.modified_count:
            logger.info(f"Favourite aggiornato per buyer_id={buyer_id}.")
            return 200
        logger.warning(f"Favourite non aggiornato per buyer_id={buyer_id}.")
        return 500
    


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
    
    def get_profile_info(self) -> int:
        if not self.buyer or not self.buyer.buyer_id:
            return 400
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        try:
            data = mongo_client.buyers.find_one({"_id": ObjectId(self.buyer.buyer_id)}, {"favourites": 0})
        except Exception as e:
            logger.error("Error retrieving buyer profile: %s", e)
            return 500
        if not data:
            return 404
        data["buyer_id"] = str(data.pop("_id"))
        self.buyer = Buyer(**data)
        return 200
    
    def get_buyer_by_email(self, email: str) -> int:
        if not email:
            return 400
        mongo_client = get_default_mongo_db()
        try:
            data = mongo_client.buyers.find_one({"email": email}, {"favourites": 0})
        except Exception as e:
            logger.error("Error retrieving buyer by email: %s", e)
            return 500
        if not data:
            return 404
        self.buyer = Buyer(
            buyer_id=str(data["_id"]),
            password=data["password"],
            email=data["email"],
            phone_number=data["phone_number"],
            name=data["name"],
            surname=data["surname"]
        )
        return 200

    def create_buyer(self) -> int:
        if not self.buyer:
            return 400
        mongo_client = get_default_mongo_db()
        buyer_data = self.buyer.model_dump(exclude_none=True, exclude={"buyer_id"})
        buyer_data["favourites"] = []
        try:
            result = mongo_client.buyers.insert_one(buyer_data)
        except Exception as e:
            logger.error("Error creating buyer: %s", e)
            return 500
        if result.inserted_id:
            self.buyer.buyer_id = str(result.inserted_id)
            return 201
        logger.error("Creation of buyer failed.")
        return 500
    
    def update_buyer(self, buyer: Buyer) -> int:
        if not self.buyer or not self.buyer.buyer_id:
            return 400
        mongo_client = get_default_mongo_db()
        update_data = buyer.model_dump(exclude_none=True, exclude={"buyer_id"})
        try:
            result = mongo_client.buyers.update_one(
                {"_id": ObjectId(self.buyer.buyer_id)},
                {"$set": update_data}
            )
        except Exception as e:
            logger.error("Error updating buyer with buyer_id=%s: %s", self.buyer.buyer_id, e)
        if result.modified_count:
            return 200
        logger.error("Update of buyer with buyer_id=%s failed.", self.buyer.buyer_id)
        return 500
    
    def delete_buyer_by_id(self, buyer_id: str) -> int:
        if not buyer_id:
            return 400
        mongo_client = get_default_mongo_db()
        try:
            result = mongo_client.buyers.delete_one({"_id": ObjectId(buyer_id)})
        except Exception as e:
            logger.error("Error deleting buyer by id: %s", e)
            return 500
        if result.deleted_count:
            return 200
        else:
            return 404
    
    def get_favourites(self) -> int:
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        try:
            data = mongo_client.buyers.find_one({"_id": ObjectId(self.buyer.buyer_id)}, {"favourites": 1})
        except Exception as e:
            logger.error("Error retrieving favourites for buyer_id=%s: %s", self.buyer.buyer_id, e)
            return 500
        if not data or "favourites" not in data:
            return 404
        self.buyer.favourites = [
            FavouriteProperty(
            **{"property_on_sale_id": str(fav["_id"]),
               **{k: v for k, v in fav.items() if k != "_id"}}
            )
            for fav in data.get("favourites", [])
        ]
        return 200
    
    def add_favourite(self, buyer_id: str, favourite: FavouriteProperty) -> int:
        if not buyer_id:
            return 400
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        data={"_id": ObjectId(favourite.property_on_sale_id), **favourite.model_dump(exclude={"property_on_sale_id"})}
        try:
            result = mongo_client.buyers.update_one(
            {"_id": ObjectId(buyer_id)},
            {"$push": {"favourites": data}}
            )
        except Exception as e:
            logger.error("Error adding favourite for buyer_id=%s: %s", buyer_id, e)
            return 500
        if result.modified_count:
            return 200
        logger.error("Addition of favourite for buyer_id=%s failed.", buyer_id)
        return 500

    def update_favourite(self, buyer_id: str, property_on_sale_id: str, updated_data: dict) -> int:
        if not buyer_id or not property_on_sale_id:
            return 400
        mongo_client = get_default_mongo_db()
        try:
            result = mongo_client.buyers.update_one(
                {"_id": ObjectId(buyer_id), "favourites.property_on_sale_id": property_on_sale_id},
                {"$set": {"favourites.$": updated_data}}
            )
        except Exception as e:
            logger.error("Error updating favourite for buyer_id=%s: %s", buyer_id, e)
            return 500
        if result.modified_count:
            return 200
        logger.error("Update of favourite for buyer_id=%s failed.", buyer_id)
        return 500
    
    def delete_favourite(self, buyer_id: str, property_on_sale_id: str) -> int:
        if not buyer_id or not property_on_sale_id:
            return 400
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        try:
            result = mongo_client.buyers.update_one(
                {"_id": ObjectId(buyer_id)},
                {"$pull": {"favourites": {"_id": ObjectId(property_on_sale_id)}}}
            )
        except Exception as e:
            logger.error("Error deleting favourite for buyer_id=%s: %s", buyer_id, e)
            return 500
        if result.modified_count:
            return 200
        logger.error("Deletion of favourite for buyer_id=%s failed.", buyer_id)
        return 500
    


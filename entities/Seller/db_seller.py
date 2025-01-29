from typing import Optional
from datetime import datetime
from bson.objectid import ObjectId
from setup.mongo_setup.mongo_setup import get_default_mongo_db
from entities.Seller.seller import Seller

class DBSeller:
    def __init__(self, seller: Optional[Seller] = None):
        self.seller = seller
    
    def create_seller(self) -> int:
        if not self.seller:
            return 400
        mongo_client = get_default_mongo_db()
        result = mongo_client.Seller.insert_one(
            self.seller.model_dump(exclude_none=True, exclude={"seller_id"})
        )
        if result.inserted_id:
            self.seller.seller_id = str(result.inserted_id)
            return 201
        return 500

    def get_seller_by_id(self) -> int:
        try:
            id = ObjectId(self.seller.seller_id)
        except:
            return 400
        mongo_client = get_default_mongo_db()
        result = mongo_client.Seller.find_one({"_id": id})
        if not result:
            return 404
        self.seller = Seller(**result)
        return 200

    def update_seller_by_id(self) -> int:
        try:
            id = ObjectId(self.seller.seller_id)
        except:
            return 400
        mongo_client = get_default_mongo_db()
        result = mongo_client.Seller.update_one(
            {"_id": id},
            {"$set": self.seller.model_dump(exclude_none=True, exclude={"seller_id"})}
        )
        if result.matched_count == 0:
            return 404
        return 200

    def delete_seller_by_id(self) -> int:
        try:
            id = ObjectId(self.seller.seller_id)
        except:
            return 400
        mongo_client = get_default_mongo_db()
        result = mongo_client.Seller.delete_one({"_id": id})
        if result.deleted_count == 0:
            return 404
        return 200


    
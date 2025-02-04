from typing import Optional
from datetime import datetime
from bson.objectid import ObjectId
from setup.mongo_setup.mongo_setup import get_default_mongo_db
from entities.MongoDB.Seller.seller import Seller, SoldProperty
import logging


logger = logging.getLogger(__name__)

class SellerDB:
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
        #change name of the key "_id" to "seller_id"
        result["seller_id"] = str(result.pop("_id"))
        self.seller = Seller(**result)
        return 200
    
    def get_seller_by_email(self, email: str) -> int:
        if not email:
            logger.error("Email not given.")
            return 400
        mongo_client = get_default_mongo_db()
        result = mongo_client.Seller.find_one({"email": email}, {"properties_on_sale": 0, "sold_properties": 0})
        if not result:
            logger.warning(f"Seller with email {email} not found.")
            return 404
        result["seller_id"] = str(result.pop("_id"))
        self.seller = Seller(**result)
        logger.debug(f"Seller retrieved: {self.seller}")
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
    
    #CONSISTENT
    def db_sell_property(self, id: ObjectId) -> int:
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return 500
        #retrive information of the property on sale from property_on_sale collection
        property_on_sale = mongo_client.PropertyOnSale.find_one({"_id": id})
        if property_on_sale is None:
            return 404
        sold_property = SoldProperty(city=property_on_sale["city"], neighbourhood=property_on_sale["neighbourhood"],price=property_on_sale["price"],thumbnail=property_on_sale["thumbnail"],type=property_on_sale["type"],area=property_on_sale["area"],registration_date=property_on_sale["registration_date"],sell_date=datetime.now())
        #add the sold_property to the sold_properties of the seller
        data= sold_property.model_dump(exclude={"sold_property_id"})
        #add the _id field to data at the beginning of the dictionary
        data = {"_id": id, **data}
        #delete the property from the properties_on_sale of the seller 
        result = mongo_client.Seller.update_one({"_id": ObjectId("67a24123e4e677efc3af0032")}, {"$pull": {"properties_on_sale": {"_id": id}}})
        if result.matched_count == 0:
            return 404
        #delete the property from the property_on_sale collection
        result = mongo_client.PropertyOnSale.delete_one({"_id": id})
        result = mongo_client.Seller.update_one({"_id": ObjectId("67a24123e4e677efc3af0032")}, {"$push": {"sold_properties": data}})
        return 200
    
    def get_sold_properties_by_price_desc(self) -> int:
        mongo_client = get_default_mongo_db()
        result = mongo_client.Seller.find_one({"_id": ObjectId("67a24123e4e677efc3af0032")})
        if not result:
            return 404
        #sort the sold_properties by price in descending order
        result["sold_properties"] = sorted(result["sold_properties"], key=lambda x: x["price"], reverse=True)
        self.seller = Seller(**result)
        return 200


        


    
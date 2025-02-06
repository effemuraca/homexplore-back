from typing import Optional
from datetime import datetime
from bson.objectid import ObjectId
from setup.mongo_setup.mongo_setup import get_default_mongo_db
from entities.MongoDB.Seller.seller import Seller, SoldProperty, SellerPropertyOnSale
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
    
    # route del seller (get_profile_info) CONSISTENT
    def get_profile_info(self) -> int:
        try:
            id = ObjectId(self.seller.seller_id)
        except:
            return 400
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return 500
        try:
            result = mongo_client.Seller.find_one({"_id": id}, {"properties_on_sale": 0, "sold_properties": 0})
        except Exception as e:
            logger.error(f"Error retrieving seller: {e}")
            return 500
        if not result:
            return 404
        #change name of the key "_id" to "seller_id"
        result["seller_id"] = str(result.pop("_id"))
        self.seller = Seller(**result)
        return 200

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
    

    # route del seller (get_properties_on_sale) CONSISTENT
    def get_properties_on_sale(self, seller: str) -> dict:
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return {"status": 500}
        try:
            result = mongo_client.Seller.find_one({"_id": ObjectId(seller)}, {"properties_on_sale": 1})
        except Exception as e:
            logger.error(f"Error retrieving properties on sale: {e}")
            return {"status": 500}
        if not result:
            return {"status": 404}
        #change the name of the key "_id" to "property_on_sale_id"
        for property_on_sale in result["properties_on_sale"]:
            property_on_sale["property_on_sale_id"] = str(property_on_sale.pop("_id"))
        return {"status": 200, "properties_on_sale": result["properties_on_sale"]}

    
    #route del seller (get_sold_properties) CONSISTENT
    def get_sold_properties(self, seller : str) -> dict:
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return {"status": 500}
        try:
            result = mongo_client.Seller.find_one({"_id": ObjectId(seller)}, {"sold_properties": 1})
        except Exception as e:
            logger.error(f"Error retrieving sold properties: {e}")
            return {"status": 500}
        if not result:
            return {"status": 404}
        
        #order the sold properties by sell_date
        result["sold_properties"] = sorted(result["sold_properties"], key=lambda x: x["sell_date"], reverse=True)
        #change the name of the key "_id" to "sold_property_id"
        for sold_property in result["sold_properties"]:
            sold_property["sold_property_id"] = str(sold_property.pop("_id"))
        return {"status": 200, "sold_properties": result["sold_properties"]}
    




    # route del seller (create_property_on_sale) CONSISTENT
    def insert_property_on_sale(self, property_on_sale : SellerPropertyOnSale) -> int:
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return 500
        data=property_on_sale.model_dump(exclude_none=True, exclude={"property_on_sale_id"})
        data = {"_id": ObjectId(property_on_sale.property_on_sale_id), **data}
        try:
            result = mongo_client.Seller.update_one(
                {"_id": ObjectId(self.seller.seller_id)},
                {"$push": {"properties_on_sale": data}}
            )
        except Exception as e:
            logger.error(f"Error inserting property on sale: {e}")
            return 500
        if result.matched_count == 0:
            return 500 #l'utente c'era fino ad un momento fa, quindi se non lo trovo è un errore
        return 200
    
    # route del seller (update_property_on_sale) CONSISTENT
    def update_property_on_sale(self, property_on_sale : SellerPropertyOnSale) -> int:
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return 500
        #data preparation 
        a=(property_on_sale.city is not None or property_on_sale.neighbourhood is not None or property_on_sale.address is not None or property_on_sale.price is not None or property_on_sale.thumbnail is not None)
        b=(property_on_sale.disponibility is not None)
        if a: 
            single_data_seller = {
                f"properties_on_sale.$.{field}": value
                for field, value in {
                    "city": property_on_sale.city,
                    "neighbourhood": property_on_sale.neighbourhood,
                    "address": property_on_sale.address,
                    "price": property_on_sale.price,
                    "thumbnail": property_on_sale.thumbnail,
                }.items()
                if value is not None
            }
        if b:
            disponibility_data_seller = {
                f"properties_on_sale.$.disponibility.{field}": value
                for field, value in {
                    "day": property_on_sale.disponibility.day,
                    "time": property_on_sale.disponibility.time,
                    "max_attendees": property_on_sale.disponibility.max_attendees,
                }.items()
                if value is not None
            }
        update_set = {}
        if a:
            update_set |= single_data_seller
        if b:
            update_set |= disponibility_data_seller
        try:
            result = mongo_client.Seller.update_one(
                {"_id": ObjectId(self.seller.seller_id), "properties_on_sale._id": ObjectId(property_on_sale.property_on_sale_id)},
                {"$set": update_set}
            )
        except Exception as e:
            logger.error(f"Error updating property on sale: {e}")
            return 500
        if result.matched_count == 0:
            return 404 
        return 200


    # route del seller (sell_property) CONSISTENT
    def sell_property(self, property : SoldProperty) -> int:
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return 500
        id_p=ObjectId(property.sold_property_id)
        id_s=ObjectId(self.seller.seller_id)
        
        #insert the sold property in the sold_properties collection
        try:
            result = mongo_client.Seller.update_one({"_id": id_s},{"$push": {"sold_properties": {"_id":id_p,**property.model_dump(exclude={"sold_property_id"})}}})
        except Exception as e:
            logger.error(f"Error adding sold property: {e}")
            return 500
        if result.matched_count == 0:
            return 404 #non existent seller
        
        #remove the property from the properties_on_sale collection
        try:
            mongo_client.Seller.update_one({"_id": id_s}, {"$pull": {"properties_on_sale": {"_id": id_p}}})
        except Exception as e:
            logger.error(f"Error removing property from 'properties_on_sale': {e}")
            #rollback all the previous operations
            try:
                mongo_client.Seller.update_one({"_id": id_s}, {"$pull": {"sold_properties": {"_id": id_p}}})
            except Exception as e:
                logger.error(f"Error rolling back: {e}")
                return 500
            logger.error("Rollback successful")
            return 500
        
        #property not on seller collection
        if result.matched_count == 0:
            #rollback all the previous operations
            try:
                mongo_client.Seller.update_one({"_id": id_s}, {"$pull": {"sold_properties": {"_id": id_p}}})
            except Exception as e:
                logger.error(f"Error rolling back: {e}")
                return 500
            logger.error("Rollback successful")
            return 404
        return 200
    
    # route del seller (delete_property_on_sale) CONSISTENT
    def delete_embedded(self, property_on_sale_id : str) -> int:
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return 500
        try:
            result = mongo_client.Seller.update_one(
                {"_id": ObjectId(self.seller.seller_id)},
                {"$pull": {"properties_on_sale": {"_id": ObjectId(property_on_sale_id)}}}
            )
        except Exception as e:
            logger.error(f"Error deleting property on sale: {e}")
            return 500
        if result.matched_count == 0:
            return 404
        return 200
        


    
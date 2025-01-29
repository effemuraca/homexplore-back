from typing import Optional
from bson.objectid import ObjectId
from entities.PropertyOnSale.property_on_sale import PropertyOnSale
from setup.mongo_setup.mongo_setup import get_default_mongo_db
from datetime import datetime



class PropertyOnSaleDB:
    def __init__(self, property_on_sale: Optional[PropertyOnSale] = None):
        self.property_on_sale = property_on_sale
    
    def create_property_on_sale(self) -> int:
        # check users information
        if not self.property_on_sale:
            return 400
        self.property_on_sale.registration_date = datetime.now()
        mongo_client = get_default_mongo_db()
        result = mongo_client.PropertyOnSale.insert_one(self.property_on_sale.model_dump(exclude_none=True, exclude={"property_on_sale_id"}))
        if result.inserted_id:
            self.property_on_sale.property_on_sale_id = str(result.inserted_id)
            return 201
        return 500
    
    def get_property_on_sale_by_id(self, property_on_sale_id:str) -> int:
        try:
            id=ObjectId(property_on_sale_id)
        except:
            return 400
        mongo_client = get_default_mongo_db()
        result = mongo_client.PropertyOnSale.find_one({"_id": id})
        if not result:
            return 404
        self.property_on_sale = PropertyOnSale(**result, property_on_sale_id=str(result["_id"]))
        return 200
    
    def delete_property_on_sale_by_id(self, property_on_sale_id:str) -> int:
        try:
            id=ObjectId(property_on_sale_id)
        except:
            return 400
        mongo_client = get_default_mongo_db()
        result = mongo_client.PropertyOnSale.delete_one({"_id": id})
        if result.deleted_count == 0:
            return 404
        return 200
    
    def update_property_on_sale(self) -> int:
        try:
            id=ObjectId(self.property_on_sale.property_on_sale_id)
        except:
            return 400
        mongo_client = get_default_mongo_db()
        result = mongo_client.PropertyOnSale.update_one({"_id": id}, {"$set": self.property_on_sale.model_dump(exclude_none=True, exclude={"property_on_sale_id"})})
        if result.matched_count == 0:
            return 404
        return 200
    
    

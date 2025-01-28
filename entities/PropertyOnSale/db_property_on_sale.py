from typing import Optional
from bson.objectid import ObjectId
from entities.PropertyOnSale.property_on_sale import PropertyOnSale
from setup.mongo_setup.mongo_setup import get_default_mongo_db
from datetime import date



class PropertyOnSaleDB:
    def __init__(self, property_on_sale: Optional[PropertyOnSale] = None):
        self.property_on_sale = property_on_sale
    
    def create_property_on_sale(self) -> int:
        # check users information
        if not self.property_on_sale:
            return 400
        if not self.property_on_sale.check_min_info():
            return 400
        self.property_on_sale.registration_date = date.today()
        mongo_client = get_default_mongo_db()
        result = mongo_client.PropertyOnSale.insert_one(self.property_on_sale.model_dump(exclude_none=True, exclude={"property_on_sale_id"}))
        if result.inserted_id:
            self.property_on_sale.property_on_sale_id = str(result.inserted_id)
            return 201
        return 500
    
    def get_property_on_sale_by_id(self) -> int:
        mongo_client = get_default_mongo_db()
        result = mongo_client.PropertyOnSale.find_one({"_id": ObjectId(self.property_on_sale.property_on_sale_id)})
        if not result:
            return 400
        self.property_on_sale = PropertyOnSale(**result)
        return 201
    
    

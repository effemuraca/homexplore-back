from typing import Optional, List
from bson.objectid import ObjectId
from entities.MongoDB.PropertyOnSale.property_on_sale import PropertyOnSale
from setup.mongo_setup.mongo_setup import get_default_mongo_db
from datetime import datetime
import logging
from modules.Guest.models.guest_models import FilteredSearchInput
from modules.RegisteredUser.models.registered_user_models import Analytics1Input

logger = logging.getLogger(__name__)

class PropertyOnSaleDB:
    def __init__(self, property_on_sale: Optional[PropertyOnSale] = None, property_on_sale_list: Optional[List[PropertyOnSale]] = None):
        self.property_on_sale = property_on_sale
        self.property_on_sale_list = property_on_sale_list
        self.analytics_1_result = None
        self.analytics_4_result = None
        self.analytics_5_result = None

    #guest route (filtered_search) CONSISTENT
    def filtered_search(self, input : FilteredSearchInput) -> int:
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        query = {}
        if input.city:
            query["city"] = input.city
        if input.max_price:
            query["price"] = {"$lte": input.max_price}
        if input.neighbourhood:
            query["neighbourhood"] = input.neighbourhood
        if input.type:
            query["type"] = input.type
        if input.min_area:
            query["area"] = {"$gte": input.min_area}
        if input.min_bed_number:
            query["bed_number"] = {"$gte": input.min_bed_number}
        if input.min_bath_number:
            query["bath_number"] = {"$gte": input.min_bath_number}
        try:
            results = mongo_client.PropertyOnSale.find(query)
        except Exception as e:
            logger.error("Error while searching: %s", e)
            return 500
        results_list = list(results)
        if not results_list:
            return 404
        self.property_on_sale_list = []
        for result in results_list:
            result["property_on_sale_id"] = str(result["_id"])
            self.property_on_sale_list.append(PropertyOnSale(**result))
        return 200
    
    #guest route (get_10_random_properties) CONSISTENT
    def get_10_random_properties(self) -> int:
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        try:
            results = mongo_client.PropertyOnSale.aggregate([{"$sample": {"size": 10}}])
        except Exception as e:
            logger.error("Error while retrieving random properties: %s", e)
            return 500
        results_list = list(results)
        if not results_list:
            return 404
        self.property_on_sale_list = []
        for result in results_list:
            result["property_on_sale_id"] = str(result["_id"])
            self.property_on_sale_list.append(PropertyOnSale(**result))
        return 200
    
    #guest route (get_property_on_sale_by_address) CONSISTENT
    def get_property_on_sale_by_address(self, city: str, address: str) -> int:
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        try:
            result = mongo_client.PropertyOnSale.find({"city": city, "address": {"$regex": address, "$options": "i"}})
        except Exception as e:
            logger.error("Error while searching property by address: %s", e)
            return 500
        if not result:
            return 404
        results_list = list(result)
        if not results_list:
            return 404
        self.property_on_sale_list = []
        for result in results_list:
            result["property_on_sale_id"] = str(result["_id"])
            if result["disponibility"]:
                # remove disponibility from the result
                result["disponibility"] = None
            self.property_on_sale_list.append(PropertyOnSale(**result))
        return 200
    
    #route del seller (delete_property_on_sale) CONSISTENT
    def delete_property_on_sale_by_id(self, property_on_sale_id:str) -> int:
        try:
            id=ObjectId(property_on_sale_id)
        except:
            return 400
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        try:
            result = mongo_client.PropertyOnSale.delete_one({"_id": id})
        except Exception as e:
            logger.error("Error deleting property on sale: %s", e)
            return 500
        if result.deleted_count == 0:
            return 404
        return 200
    
    #route del seller (create_property_on_sale) CONSISTENT
    def create_property_on_sale(self) -> int:
        if not self.property_on_sale:
            return 400
        self.property_on_sale.registration_date = datetime.now()
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        try:
            result = mongo_client.PropertyOnSale.insert_one(self.property_on_sale.model_dump(exclude_none=True, exclude={"property_on_sale_id"}))
        except Exception as e:
            logger.error("Error during property creation: %s", e)
            return 500
        if result.inserted_id:
            self.property_on_sale.property_on_sale_id = str(result.inserted_id)
            return 200
        logger.error("Property not created")
        return 500
    
    # route seller (update_property_on_sale) CONSISTENT
    def update_property_on_sale(self) -> int:
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        # data preparation
        id=ObjectId(self.property_on_sale.property_on_sale_id)
        single_data = self.property_on_sale.model_dump(exclude_none=True, exclude={"property_on_sale_id", "photos", "disponibility"})
        a= (self.property_on_sale.city is not None or self.property_on_sale.neighbourhood is not None or self.property_on_sale.address is not None or self.property_on_sale.price is not None or self.property_on_sale.thumbnail is not None or self.property_on_sale.type is not None or self.property_on_sale.area is not None or self.property_on_sale.registration_date is not None or self.property_on_sale.bed_number is not None or self.property_on_sale.bath_number is not None or self.property_on_sale.description is not None)
        b= (self.property_on_sale.photos is not None)
        c= (self.property_on_sale.disponibility is not None)
        if c:
            disponibility_data_property = {
                f"disponibility.{field}": value
                for field, value in {
                    "day": self.property_on_sale.disponibility.day,
                    "time": self.property_on_sale.disponibility.time,
                    "max_attendees": self.property_on_sale.disponibility.max_attendees,
                }.items()
                if value is not None
            }
        set_fields = {}
        push_fields = {}

        if a:
            set_fields |= single_data
        if c:
            set_fields |= disponibility_data_property
        if b:
            push_fields["photos"] = {"$each": self.property_on_sale.photos}

        update_data = {}
        if set_fields:
            update_data["$set"] = set_fields
        if push_fields:
            update_data["$push"] = push_fields

        try:
            result = mongo_client.PropertyOnSale.update_one({"_id": id}, update_data)
        except Exception as e:
            logger.error("Error updating property on sale: %s", e)
            return 500
        if result.matched_count == 0:
            return 404
        return 200
    
    # seller route (sell_property) CONSISTENT
    def get_property_on_sale_by_id(self, property_on_sale_id:str) -> int:
        if not ObjectId.is_valid(property_on_sale_id):
            return 400
        id=ObjectId(property_on_sale_id)
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        try:
            result = mongo_client.PropertyOnSale.find_one({"_id": id})
        except Exception as e:
            logger.error("Error retrieving property on sale with id: %s, error: %s", property_on_sale_id, e)
            return 500
        if not result:
            return 404
        self.property_on_sale = PropertyOnSale(**result, property_on_sale_id=str(result["_id"]))
        return 200
    
    # seller route (sell_property) CONSISTENT
    def delete_and_return_property(self, property_on_sale_id:str) -> int:
        id=ObjectId(property_on_sale_id)
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        try:
            result = mongo_client.PropertyOnSale.find_one_and_delete({"_id": id})
        except Exception as e:
            logger.error("Error deleting property on sale with id: %s, error: %s", property_on_sale_id, e)
            return 500
        if not result:
            return 404
        self.property_on_sale = PropertyOnSale(**result, property_on_sale_id=str(result["_id"]))
        return 200
    

    # seller route (sell_property) CONSISTENT
    def insert_property(self) -> int:
        if not self.property_on_sale:
            return 400
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        try:
            result=mongo_client.PropertyOnSale.insert_one({"_id": ObjectId(self.property_on_sale.property_on_sale_id), **self.property_on_sale.model_dump(exclude_none=True, exclude={"property_on_sale_id"})})
        except Exception as e:
            logger.error("Error inserting property on sale: %s", e)
            return 500
        if result.inserted_id == self.property_on_sale.property_on_sale_id:
            return 200
        else:
            logger.error("Error inserting property on sale with id: %s", self.property_on_sale.property_on_sale_id)
            return 500
        
    def get_analytics_1(self, input: Analytics1Input) -> int:
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        try:
            pipeline = [
                {"$match": input.model_dump(exclude_none=True, exclude={"order_by"})},
                {"$project": {"neighbourhood": 1, "price_per_square_meter": {"$divide": ["$price", "$area"]}}},
                {"$group": {"_id": "$neighbourhood", "avg_price": {"$avg": "$price_per_square_meter"}}},
                {"$project": {"neighbourhood": "$_id", "avg_price": 1, "_id": 0}},
                {"$sort": {"avg_price": input.order_by}}
            ]
            aggregation_result = mongo_client.PropertyOnSale.aggregate(pipeline)
        except Exception as e:
            logger.error("Error during analytics_1: %s", e)
            return 500
        
        if not aggregation_result:
            return 404
        
        self.analytics_1_result = list(aggregation_result)
        return 200
    
    
    def get_analytics_4(self, city: str):
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        try:
            pipeline = [
                {"$match": {"city": city}},
                {"$project": {"type": 1, "price": 1}},
                {"$group": {"_id": "$type", "avg_price": {"$avg": "$price"}, "count": {"$sum": 1}}},
                {"$project": {"type": "$_id", "avg_price": 1, "_id": 0, "count": 1}}
            ]
            aggregation_result = mongo_client.PropertyOnSale.aggregate(pipeline)
        except Exception as e:
            logger.error("Error during analytics_4: %s", e)
            return 500
        if not aggregation_result:
            return 404
        self.analytics_4_result = list(aggregation_result)
        return 200
        
    def get_analytics_5(self, city: str, neighbourhood: str):
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        try:
            pipeline = [
            # average bed_number, bath_number and area for each type of property
                {"$match": {"city": city, "neighbourhood": neighbourhood}},
                {"$group": {"_id": "$type", "avg_bed_number": {"$avg": "$bed_number"}, "avg_bath_number": {"$avg": "$bath_number"}, "avg_area": {"$avg": "$area"}}},
                {"$project": {"type": "$_id", "avg_bed_number": 1, "avg_bath_number": 1, "avg_area": 1, "_id": 0}}
            ]
            aggregation_result = mongo_client.PropertyOnSale.aggregate(pipeline)
        except Exception as e:
            logger.error("Error during analytics_5: %s", e)
            return 500
        if not aggregation_result:
            return 404
        self.analytics_5_result = list(aggregation_result)
        return 200
        
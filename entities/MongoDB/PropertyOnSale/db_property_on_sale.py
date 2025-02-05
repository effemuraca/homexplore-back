from typing import Optional, List
from bson.objectid import ObjectId
from entities.MongoDB.PropertyOnSale.property_on_sale import PropertyOnSale
from setup.mongo_setup.mongo_setup import get_default_mongo_db
from datetime import datetime
import logging


from modules.Guest.models.guest_models import FilteredSearchInput

class PropertyOnSaleDB:
    def __init__(self, property_on_sale: Optional[PropertyOnSale] = None, property_on_sale_list: Optional[List[PropertyOnSale]] = None):
        self.property_on_sale = property_on_sale
        self.property_on_sale_list = property_on_sale_list
    
    #CONSISTENT
    #creazione di property_on_sale di seller
    def create_property_on_sale(self) -> int:
        if not self.property_on_sale:
            return 400
        self.property_on_sale.registration_date = datetime.now()
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return 500
        try:
            result = mongo_client.PropertyOnSale.insert_one(self.property_on_sale.model_dump(exclude_none=True, exclude={"property_on_sale_id"}))
        except Exception as e:
            return 500
        if result.inserted_id:
            self.property_on_sale.property_on_sale_id = str(result.inserted_id)
            data = self.property_on_sale.convert_to_seller_property()
            try:
                result = mongo_client.Seller.update_one({"_id": ObjectId("67a24123e4e677efc3af0032")}, {"$push": {"properties_on_sale": data}})
            except Exception as e:
                #rollback of property creation
                try:
                    mongo_client.PropertyOnSale.delete_one({"_id": ObjectId(self.property_on_sale.property_on_sale_id)})
                except Exception as e:
                    # Log the error if needed
                    logging.error("Error during rollback for object creation of property_on_sale_id {}".format(self.property_on_sale.property_on_sale_id))
                return 500
            return 201
        return 500
    
    #get di property on sale by id  (CONTROLLATA) (guest)
    def get_property_on_sale_by_id(self, property_on_sale_id:str) -> int:
        if not ObjectId.is_valid(property_on_sale_id):
            return 400
        id=ObjectId(property_on_sale_id)
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return 500
        try:
            result = mongo_client.PropertyOnSale.find_one({"_id": id})
        except Exception as e:
            logging.error("Error retrieving property on sale with id: %s, error: %s", property_on_sale_id, e)
            return 500
        if not result:
            return 404
        self.property_on_sale = PropertyOnSale(**result, property_on_sale_id=str(result["_id"]))
        return 200
    
    #rimonazione di property_on_sale from seller
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
    
    #CONSISTENT
    #update of property_on_sale for seller
    def update_property_on_sale(self) -> int:
        try:
            id=ObjectId(self.property_on_sale.property_on_sale_id)
        except:
            return 400
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return 500
        
        #data preparation from SellerPropertyOnSale object
        seller_property= SellerPropertyOnSale(city=self.property_on_sale.city, neighbourhood=self.property_on_sale.neighbourhood, address=self.property_on_sale.address, price=self.property_on_sale.price, thumbnail=self.property_on_sale.thumbnail, disponibility=self.property_on_sale.disponibility)
        single_data_seller = {
            f"properties_on_sale.$.{field}": value
            for field, value in {
                "city": seller_property.city,
                "neighbourhood": seller_property.neighbourhood,
                "address": seller_property.address,
                "price": seller_property.price,
                "thumbnail": seller_property.thumbnail,
            }.items()
            if value is not None
        }
        if self.property_on_sale.disponibility is not None:
            disponibility = self.property_on_sale.disponibility
            disponibility_data_property = {
                f"disponibility.{field}": value
                for field, value in {
                    "day": disponibility.day,
                    "time": disponibility.time,
                    "max_attendees": disponibility.max_attendees,
                }.items()
                if value is not None
            }
            disponibility_data_seller = {
                f"properties_on_sale.$.disponibility.{field}": value
                for field, value in {
                    "day": disponibility.day,
                    "time": disponibility.time,
                    "max_attendees": disponibility.max_attendees,
                }.items()
                if value is not None
            }
        
        a=(seller_property.city is not None or seller_property.neighbourhood is not None or seller_property.address is not None or seller_property.price is not None or seller_property.thumbnail is not None)
        b=(seller_property.disponibility is not None)
        
        update_set = {}
        if a:
            update_set |= single_data_seller
        if b:
            update_set |= disponibility_data_seller

        result = mongo_client.Seller.update_one(
            {"_id": ObjectId("679a41fa777bc4a7eb04807a"), "properties_on_sale._id": id},
            {"$set": update_set}
        )

        #data preparation from PropertyOnSale object
        single_data = self.property_on_sale.model_dump(exclude_none=True, exclude={"property_on_sale_id", "photos", "disponibility"})
        a= (self.property_on_sale.city is not None or self.property_on_sale.neighbourhood is not None or self.property_on_sale.address is not None or self.property_on_sale.price is not None or self.property_on_sale.thumbnail is not None or self.property_on_sale.type is not None or self.property_on_sale.area is not None or self.property_on_sale.registration_date is not None or self.property_on_sale.bed_number is not None or self.property_on_sale.bath_number is not None or self.property_on_sale.description is not None)
        b= (self.property_on_sale.photos is not None)
        c= (self.property_on_sale.disponibility is not None)
        
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

        result = mongo_client.PropertyOnSale.update_one({"_id": id}, update_data)

        if result.matched_count == 0:
            return 404
        return 200
    

    #Ricerca filtrata delle proprietà in vendita (CONTOLLATA) (guest)
    def filtered_search(self, input : FilteredSearchInput) -> int:
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
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
            logging.error("Error while searching: %s", e)
            return 500
        results_list = list(results)
        if not results_list:
            return 404
        self.property_on_sale_list = []
        for result in results_list:
            result["property_on_sale_id"] = str(result["_id"])
            self.property_on_sale_list.append(PropertyOnSale(**result))
        return 200
    
    #Ricerca di 10 proprietà casuali (CONTROLLATA) (guest
    def get_10_random_properties(self) -> int:
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return 500
        try:
            results = mongo_client.PropertyOnSale.aggregate([{"$sample": {"size": 10}}])
        except Exception as e:
            logging.error("Error while retrieving random properties: %s", e)
            return 500
        results_list = list(results)
        if not results_list:
            return 404
        self.property_on_sale_list = []
        for result in results_list:
            result["property_on_sale_id"] = str(result["_id"])
            self.property_on_sale_list.append(PropertyOnSale(**result))
        return 200
    
    #Ricerca di una proprietà per indirizzo e città (CONTROLLATA) (guest)
    def get_property_on_sale_by_address(self, city: str, address: str) -> int:
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return 500
        try:
            result = mongo_client.PropertyOnSale.find_one({"city": city, "address": address})
        except Exception as e:
            logging.error("Error while searching property by address: %s", e)
            return 500
        if not result:
            return 404
        result["property_on_sale_id"] = str(result["_id"])
        self.property_on_sale = PropertyOnSale(**result)
        return 200
    


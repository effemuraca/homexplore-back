from typing import Optional
from bson.objectid import ObjectId
from entities.PropertyOnSale.property_on_sale import PropertyOnSale
from setup.mongo_setup.mongo_setup import get_default_mongo_db
from datetime import datetime
from entities.Seller.seller import SellerPropertyOnSale


class PropertyOnSaleDB:
    def __init__(self, property_on_sale: Optional[PropertyOnSale] = None):
        self.property_on_sale = property_on_sale
    
    #CONSISTENT
    def create_property_on_sale(self) -> int:
        if not self.property_on_sale:
            return 400
        self.property_on_sale.registration_date = datetime.now()
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return 500
        result = mongo_client.PropertyOnSale.insert_one(self.property_on_sale.model_dump(exclude_none=True, exclude={"property_on_sale_id"}))
        if result.inserted_id:
            self.property_on_sale.property_on_sale_id = str(result.inserted_id)
            data={
                "_id": ObjectId(self.property_on_sale.property_on_sale_id),
                "city": self.property_on_sale.city,
                "neighbourhood": self.property_on_sale.neighbourhood,
                "address": self.property_on_sale.address,
                "price": self.property_on_sale.price,
                "thumbnail": self.property_on_sale.thumbnail,
            }
            if self.property_on_sale.disponibility:
                data["disponibility"] = self.property_on_sale.disponibility.model_dump()
            result = mongo_client.Seller.update_one({"_id": ObjectId("679a41fa777bc4a7eb04807a")}, {"$push": {"properties_on_sale": data}})
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
    
    #CONSISTENT
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
    
    def filtered_search(self, city: str, max_price: int, neighbourhood: str, type: str, area: int, min_bed_number: int, min_bath_number: int) -> int:
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return 500
        query = {}
        if city:
            query["city"] = city
        if max_price:
            query["price"] = {"$lte": max_price}
        if neighbourhood:
            query["neighbourhood"] = neighbourhood
        if type:
            query["type"] = type
        if area:
            query["area"] = {"$gte": area}
        if min_bed_number:
            query["bed_number"] = {"$gte": min_bed_number}
        if min_bath_number:
            query["bath_number"] = {"$gte": min_bath_number}
        results = mongo_client.PropertyOnSale.find(query)
        results_list = list(results)
        from entities.PropertyOnSale.property_on_sale import PropertyOnSale
        properties = []
        for result in results_list:
            result["property_on_sale_id"] = str(result["_id"])
            properties.append(PropertyOnSale(**result))
        self.property_on_sale = properties
        return 200
    
    def get_10_random_properties(self) -> int:
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return 500
        results = mongo_client.PropertyOnSale.aggregate([{"$sample": {"size": 10}}])
        results_list = list(results)
        from entities.PropertyOnSale.property_on_sale import PropertyOnSale
        properties = []
        for result in results_list:
            result["property_on_sale_id"] = str(result["_id"])
            properties.append(PropertyOnSale(**result))
        self.property_on_sale = properties
        return 200
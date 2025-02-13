from typing import Optional
from datetime import datetime
from bson.objectid import ObjectId
from setup.mongo_setup.mongo_setup import get_default_mongo_db
from entities.MongoDB.Seller.seller import Seller, SoldProperty, SellerPropertyOnSale
from modules.Seller.models.seller_models import Analytics2Input, Analytics3Input
from modules.Seller.models.response_models import OpenHouseOccurrence
import logging

logger = logging.getLogger(__name__)

class SellerDB:
    def __init__(self, seller: Optional[Seller] = None):
        self.seller = seller
        self.current_open_house_events = None
        self.analytics_2_result = None
        self.analytics_3_result = None
    
    def create_seller(self) -> int:
        """
        Create a new seller in the MongoDB.

        Returns:
            int: 201 if the seller is created successfully,
                 400 if seller is not provided,
                 500 if there's an error during insertion.
        """
        if not self.seller:
            return 400
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        try:
            result = mongo_client.Seller.insert_one(
                self.seller.model_dump(exclude_none=True, exclude={"seller_id"})
            )
        except Exception as e:
            logger.error(f"Error inserting seller: {e}")
            return 500
        if result.inserted_id:
            self.seller.seller_id = str(result.inserted_id)
            return 201
        logger.error("Creation of seller with email %s failed.", self.seller.email)
        return 500
    
    # route del seller (get_profile_info) CONSISTENT
    def get_profile_info(self) -> int:
        """
        Retrieve the profile information of the seller, excluding properties_on_sale and sold_properties.

        Returns:
            int: 200 if the seller information is retrieved,
                 400 if seller_id is invalid,
                 404 if seller is not found,
                 500 if a database error occurs.
        """
        try:
            id = ObjectId(self.seller.seller_id)
        except:
            return 400
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        try:
            result = mongo_client.Seller.find_one({"_id": id}, {"properties_on_sale": 0, "sold_properties": 0})
        except Exception as e:
            logger.error(f"Error retrieving seller with id {self.seller.seller_id}: {e}")
            return 500
        if not result:
            return 404
        result["seller_id"] = str(result.pop("_id"))
        self.seller = Seller(**result)
        return 200

    def get_seller_by_id(self) -> int:
        """
        Retrieve the seller information by seller_id.

        Returns:
            int: 200 if seller is found,
                 400 if seller_id is invalid,
                 404 if seller is not found,
                 500 if a database error occurs.
        """
        try:
            id = ObjectId(self.seller.seller_id)
        except:
            return 400
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        try:
            result = mongo_client.Seller.find_one({"_id": id})
        except Exception as e:
            logger.error(f"Error retrieving seller with id {self.seller.seller_id}: {e}")
            return 500
        if not result:
            return 404
        result["seller_id"] = str(result.pop("_id"))
        self.seller = Seller(**result)
        return 200
    
    def get_seller_by_email(self, email: str) -> int:
        """
        Retrieve the seller information by email.

        Args:
            email (str): The email of the seller.
        
        Returns:
            int: 200 if seller is found,
                 400 if email is not provided,
                 404 if seller is not found,
                 500 if a database error occurs.
        """
        if not email:
            return 400
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        try:
            result = mongo_client.Seller.find_one({"email": email}, {"properties_on_sale": 0, "sold_properties": 0})
        except Exception as e:
            logger.error(f"Error retrieving seller with email {email}: {e}")
            return 500
        if not result:
            return 404
        result["seller_id"] = str(result.pop("_id"))
        self.seller = Seller(**result)
        return 200

    def update_seller(self, seller: Seller) -> int:
        """
        Update seller information.

        Args:
            seller (Seller): The updated seller data.
        
        Returns:
            int: 200 if the update is successful,
                 400 if seller_id is invalid,
                 404 if seller is not found,
                 500 if a database error occurs.
        """
        try:
            id = ObjectId(self.seller.seller_id)
        except:
            return 400
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        try:
            result = mongo_client.Seller.update_one(
                {"_id": id},
                {"$set": seller.model_dump(exclude_none=True, exclude={"seller_id"})}
            )
        except Exception as e:
            logger.error(f"Error updating seller with id {self.seller.seller_id}: {e}")
            return 500
        if result.matched_count == 0:
            return 404
        return 200

    def delete_seller_by_id(self) -> int:
        """
        Delete the seller by seller_id.

        Returns:
            int: 200 if deletion is successful,
                 400 if seller_id is invalid,
                 404 if seller is not found,
                 500 if a database error occurs.
        """
        try:
            id = ObjectId(self.seller.seller_id)
        except:
            return 400
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        try:
            result = mongo_client.Seller.delete_one({"_id": id})
        except Exception as e:
            logger.error(f"Error deleting seller with id {self.seller.seller_id}: {e}")
            return 500
        if result.deleted_count == 0:
            return 404
        return 200
    

    # route del seller (get_properties_on_sale) CONSISTENT
    def get_properties_on_sale(self) -> int:
        """
        Retrieve properties on sale for the seller.

        Returns:
            int: 200 if properties are found,
                 404 if properties are not found,
                 500 if a database error occurs.
        """
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        try:
            result = mongo_client.Seller.find_one({"_id": ObjectId(self.seller.seller_id)}, {"properties_on_sale": 1})
        except Exception as e:
            logger.error(f"Error retrieving properties on sale: for seller {self.seller.seller_id}: {e}")
            return 500
        if not result or "properties_on_sale" not in result or len(result["properties_on_sale"]) == 0:
            return 404
        for property_on_sale in result["properties_on_sale"]:
            property_on_sale["property_on_sale_id"] = str(property_on_sale.pop("_id"))
        self.seller.properties_on_sale = [SellerPropertyOnSale(**property_on_sale) for property_on_sale in result["properties_on_sale"]]
        return 200
    
    def get_property_on_sale_filtered(self, city: str, neighbourhood: str, address: str) -> int:
        """
        Retrieve properties on sale for the seller filtered by city, neighbourhood, and address.

        Args:
            city (str): The city to filter by.
            neighbourhood (str): The neighbourhood to filter by.
            address (str): The address to filter by.
        
        Returns:
            int: 200 if properties matching the filter are found,
                 404 if no properties match,
                 500 if a database error occurs.
        """
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        pipeline = [
            { "$match": { "_id": ObjectId(self.seller.seller_id) } },
            { "$project": {
                "_id": 0,
                "properties_on_sale": {
                    "$filter": {
                        "input": "$properties_on_sale",
                        "as": "property",
                        "cond": {
                            "$and": [
                                { "$eq": ["$$property.city", city] } if city else {},
                                { "$eq": ["$$property.neighbourhood", neighbourhood] } if neighbourhood else {},
                                { "$eq": ["$$property.address", address] } if address else {}
                            ]
                        }
                    }
                }
            }}
        ]
        try:
            result = mongo_client.Seller.aggregate(pipeline)
        except Exception as e:
            logger.error(f"Error retrieving filtered properties for seller {self.seller.seller_id}: {e}")
            return 500
        # Extract the properties_on_sale array from the result
        properties = list(result)[0].get("properties_on_sale", [])
        if not properties:
            return 404
        for property_on_sale in properties:
            property_on_sale["property_on_sale_id"] = str(property_on_sale.pop("_id"))
        self.seller.properties_on_sale = [SellerPropertyOnSale(**property_on_sale) for property_on_sale in properties]
        return 200
    
    def get_sold_properties_filtered(self, city: str, neighbourhood: str) -> int:
        """
        Retrieve sold properties for the seller, sorted by sell_date descending.

        Returns:
            int: 200 if sold properties are found,
                 404 if sold properties are not found,
                 500 if a database error occurs.
        """
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        pipeline = [
            { "$match": { "_id": ObjectId(self.seller.seller_id) } },
            { "$project": {
                "_id": 0,
                "sold_properties": {
                    "$filter": {
                        "input": "$sold_properties",
                        "as": "property",
                        "cond": {
                            "$and": [
                                { "$eq": ["$$property.city", city] } if city else {},
                                { "$eq": ["$$property.neighbourhood", neighbourhood] } if neighbourhood else {}
                            ]
                        }
                    }
                }
            }}
        ]
        try:
            result = mongo_client.Seller.aggregate(pipeline)
        except Exception as e:
            logger.error(f"Error retrieving sold properties for seller {self.seller.seller_id}: {e}")
            return 500
        sold_properties = list(result)[0].get("sold_properties", [])
        if not sold_properties:
            return 404
        
        # Order the sold properties by sell_date
        sold_properties.sort(key=lambda x: x["sell_date"], reverse=True)
        for sold_property in sold_properties:
            sold_property["sold_property_id"] = str(sold_property.pop("_id"))
        self.seller.sold_properties = [SoldProperty(**sold_property) for sold_property in sold_properties]
        return 200
      
    def insert_property_on_sale(self, property_on_sale : SellerPropertyOnSale) -> int:
        """
        Insert a new property on sale into the seller's document.

        Args:
            property_on_sale (SellerPropertyOnSale): The property data to insert.
        
        Returns:
            int: 200 if the property is inserted successfully,
                 404 if the seller is not found,
                 500 if a database error occurs.
        """
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
            return 404
        return 200
    
    # route del seller (update_property_on_sale) CONSISTENT
    def update_property_on_sale(self, property_on_sale : SellerPropertyOnSale) -> int:
        """
        Update an existing property on sale in the seller's document.

        Args:
            property_on_sale (SellerPropertyOnSale): The property data with updated fields.
        
        Returns:
            int: 200 if the property is updated successfully,
                 404 if the property is not found,
                 500 if a database error occurs.
        """
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return 500
        # Data preparation 
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
    
    # route del seller (delete_property_on_sale) CONSISTENT
    def delete_embedded(self, property_on_sale_id : str) -> int:
        """
        Delete an embedded property on sale from the seller's document.

        Args:
            property_on_sale_id (str): The id of the property to delete.
        
        Returns:
            int: 200 if the property is deleted successfully,
                 404 if the property is not found or not modified,
                 500 if a database error occurs.
        """
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
        if result.matched_count == 0 or result.modified_count == 0:
            return 404
        return 200
    
    # route del seller (sell_property) CONSISTENT
    def sell_property(self, property: SoldProperty) -> int:
        """
        Move a property from properties_on_sale to sold_properties.

        Args:
            property (SoldProperty): The property being sold.
        
        Returns:
            int: 200 if the property is sold successfully,
                 500 if a database error occurs.
        """
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return 500

        id_p = ObjectId(property.sold_property_id)
        id_s = ObjectId(self.seller.seller_id)

        try:
            result = mongo_client.Seller.update_one(
                {"_id": id_s},
                {
                    "$push": {"sold_properties": {"_id": id_p, **property.model_dump(exclude={"sold_property_id"})}},
                    "$pull": {"properties_on_sale": {"_id": id_p}}
                }
            )
        except Exception as e:
            logger.error(f"Error selling property: {e}")
            return 500
        return 200
    

    # route del seller (sell_property) CONSISTENT
    def check_property_on_sale(self, property_on_sale_id: str) -> int:
        """
        Check whether a property on sale exists for the seller.

        Args:
            property_on_sale_id (str): The id of the property to check.
        
        Returns:
            int: 200 if the property exists,
                 500 if a database error occurs,
                 404 if the property is not found.
        """
        id_p = ObjectId(property_on_sale_id)
        id_s = ObjectId(self.seller.seller_id)
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            return 500
        try:
            result = mongo_client.Seller.find_one(
                {"_id": id_s, "properties_on_sale._id": id_p},
                {"properties_on_sale.$": 1}
            )
        except Exception as e:
            logger.error(f"Error selling property: {e}")
            return 500
        if not result:
            return 404
        return 200
    
    def get_open_house_today(self) -> int:
        """
        Retrieve open house events for the current day for the seller.
        
        The function queries the seller's document, iterates through the embedded 
        properties_on_sale list, and filters events whose 'disponibility.day' matches today's day.
        
        Returns:
            int: 200 if events are found,
                 404 if no events are found,
                 500 if a database error occurs.
        """
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        try:
            # Query the seller document for the properties on sale
            result = mongo_client.Seller.find_one(
                {"_id": ObjectId(self.seller.seller_id)},
                {"properties_on_sale": 1}
            )
        except Exception as e:
            logger.error(f"Error retrieving properties on sale for seller {self.seller.seller_id}: {e}")
            return 500

        if not result or "properties_on_sale" not in result or len(result["properties_on_sale"]) == 0:
            return 404

        # Get the current day name (e.g., Monday, Tuesday, etc.)
        current_day = datetime.now().strftime("%A")
        print(current_day)
        open_house_events = []

        # Iterate over each property on sale and check if an open house event is scheduled for today
        for prop in result["properties_on_sale"]:
            disponibility = prop.get("disponibility", {})
            if disponibility.get("day") == current_day:
                open_house_events.append({
                    "city": prop.get("city"),
                    "address": prop.get("address"),
                    "time": disponibility.get("time")
                })

        if not open_house_events:
            return 404

        self.current_open_house_events = [OpenHouseOccurrence(**event) for event in open_house_events]
        return 200 
    
    def get_sold_properties_statistics(self, input:Analytics2Input) -> int:
        """
        Retrieve sold properties statistics (houses sold and revenue) grouped by neighbourhood.

        Args:
            input (Analytics2Input): Input parameters including date range and city.
        
        Returns:
            int: 200 if statistics are retrieved successfully,
                 400 if the date range is invalid,
                 500 if a database error occurs.
        """
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        
        # Convert input dates into datetime objects
        start = datetime.strptime(input.start_date, "%Y-%m-%d")
        end = datetime.strptime(input.end_date, "%Y-%m-%d")

        # Check if the start date is before the end date
        if start > end:
            return 400
        
        pipeline = [
                {
                    "$match": {
                        "_id": ObjectId(self.seller.seller_id),
                    }
                },
                {"$unwind": "$sold_properties"},
                {
                    "$match": {
                        "sold_properties.city": input.city,
                        "sold_properties.sell_date": {"$gte": start,"$lte": end}
                    }
                },
                {
                    "$group": {
                        "_id": "$sold_properties.neighbourhood",
                        "houses_sold": {"$sum": 1},
                        "revenue": {"$sum": "$sold_properties.price"}
                    }
                },
                {
                    "$project": {
                        "neighbourhood": "$_id",
                        "houses_sold": 1,
                        "revenue": 1,
                        "_id": 0
                    }
                }
            ]
        try:
            aggregation_result = mongo_client.Seller.aggregate(pipeline)
        except Exception as e:
            logger.error(f"Error retrieving analytics 2: {e}")
            return 500
        self.analytics_2_result = list(aggregation_result)
        return 200
        
    
    def get_avg_time_to_sell(self, input:Analytics3Input) -> int:
        """
        Calculate the average time to sell properties grouped by neighbourhood.

        Args:
            input (Analytics3Input): Input parameters including start date and city.
        
        Returns:
            int: 200 if the average time is calculated successfully,
                 500 if a database error occurs.
        """
        mongo_client = get_default_mongo_db()
        if mongo_client is None:
            logger.error("Mongo client not initialized.")
            return 500
        
        start=datetime.strptime(input.start_date, "%Y-%m-%d")
        pipeline = [
                {"$match": {"_id": ObjectId(self.seller.seller_id)}},
                {"$unwind": "$sold_properties"},
                {"$match": {"sold_properties.city": input.city, "sold_properties.registration_date": {"$gte": start}}},
                {"$project": {
                    "time_to_sell": {
                        "$divide": [{"$subtract": ["$sold_properties.sell_date", "$sold_properties.registration_date"]},86400000 ]
                    },
                    "sold_properties.neighbourhood": 1
                }
                },
                {
                "$group": {
                    "_id": "$sold_properties.neighbourhood",
                    "avg_time_to_sell": {"$avg": "$time_to_sell"},
                    "num_house": {"$sum": 1}
                }    
                },
                {
                    "$project": {
                        "neighbourhood": "$_id",
                        "avg_time_to_sell": 1,
                        "num_house": 1,
                        "_id": 0
                    }
                }
            ]
        try:
            aggregation_result = mongo_client.Seller.aggregate(pipeline)
        except Exception as e:
            logger.error(f"Error retrieving analytics 3: {e}")
            return 500
        self.analytics_3_result = list(aggregation_result)
        return 200
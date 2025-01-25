from bson.objectid import ObjectId
from entities.Buyer.buyer import Buyer
from setup.mongo_setup.mongo_setup import get_default_mongo_db

class BuyerDB:
    buyer: Buyer = None

    def __init__(self, buyer: Buyer):
        self.buyer = buyer

    def get_buyer_by_id(self, buyer_id: str) -> bool:
        if not buyer_id:
            return None
        mongo_client = get_default_mongo_db()
        data = mongo_client.buyers.find_one({"_id": ObjectId(buyer_id)})
        if not data:
            return None
        self.buyer=Buyer(
            buyer_id=str(data["_id"]),
            password=data["password"],
            email=data["email"],
            phone_number=data["phone_number"],
            name=data["name"],
            surname=data["surname"],
            age=data["age"]
        )
        return True
    
    def delete_buyer_by_id(self, buyer_id: str) -> bool:
        if not buyer_id:
            return False
        mongo_client = get_default_mongo_db()
        result = mongo_client.buyers.delete_one({"_id": ObjectId(buyer_id)})
        return bool(result.deleted_count)
    


    def create_buyer(self) -> bool:
        if not self.buyer:
            return False
        mongo_client = get_default_mongo_db()
        result = mongo_client.buyers.insert_one(self.buyer.get_buyer_info())
        if not result.inserted_id:
            return False
        self.buyer.buyer_id = str(result.inserted_id)
        return bool(result.inserted_id)
    




    def update_buyer(self, buyer: Buyer = None) -> bool:
        mongo_client = get_default_mongo_db()
        # get the current data
        data = mongo_client.buyers.find_one({"_id": ObjectId(buyer.buyer_id)})
        if not data:
            return False   
        # update the data
        if buyer.password:
            data["password"] = buyer.password   
        if buyer.email:
            data["email"] = buyer.email
        if buyer.phone_number:
            data["phone_number"] = buyer.phone_number
        if buyer.name:
            data["name"] = buyer.name
        if buyer.surname:
            data["surname"] = buyer.surname
        if buyer.age:
            data["age"] = buyer.age
        # update the data in the database
        data.pop("_id", None)
        result = mongo_client.buyers.update_one({"_id": ObjectId(buyer.buyer_id)}, {"$set": data})
        return bool(result.modified_count)

    

   
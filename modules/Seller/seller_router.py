from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from entities.Seller.seller import Seller
from entities.Seller.db_seller import DBSeller
from modules.Seller.models.seller_models import CreateSeller, UpdateSeller
from modules.Seller.models import response_models as ResponseModels
from modules.PropertyOnSale.models.property_on_sale_models import UpdateDisponibility
from modules.PropertyOnSale.models.property_on_sale_models import UpdatePropertyOnSale

#import for mtethods
from setup.mongo_setup.mongo_setup import get_default_mongo_db
from bson.objectid import ObjectId
from datetime import datetime
from entities.PropertyOnSale.property_on_sale import PropertyOnSale


seller_router = APIRouter(prefix="/sellers", tags=["Sellers"])

@seller_router.post("/crud_create", response_model=ResponseModels.CreateSellerResponseModel, responses=ResponseModels.CreateSellerResponses)
def create_seller(seller: CreateSeller):
    db_seller = DBSeller(Seller(**seller.model_dump()))
    response = db_seller.create_seller()
    if response == 400:
        raise HTTPException(status_code=400, detail="Invalid seller information.")
    if response == 500:
        raise HTTPException(status_code=500, detail="Failed to create seller.")
    return JSONResponse(status_code=201, content={"detail": "Seller created successfully.", "seller_id": db_seller.seller.seller_id})

# sell a property (move it from properties_on_sale to sold_properties of the seller & delete it from the property_on_sale collection)
@seller_router.post("/methods/sell_property", response_model=ResponseModels.SuccessModel)
def sell_property(property_to_sell_id: str):
    mongo_client = get_default_mongo_db()
    if mongo_client is None:
        raise HTTPException(status_code=500, detail="Failed to connect to database.")
    result = mongo_client.Seller.find_one({"_id": ObjectId("679a41fa777bc4a7eb04807a")})
    if not result:
        raise HTTPException(status_code=404, detail="Seller not found.")
    #check throw the properties_on_sale of the seller to find the property to sell 
    for property_on_sale in result["properties_on_sale"]:
        if property_on_sale["_id"] == ObjectId(property_to_sell_id):
            #delete the property from the properties_on_sale
            result = mongo_client.Seller.update_one({"_id": ObjectId("679a41fa777bc4a7eb04807a")}, {"$pull": {"properties_on_sale": {"_id": ObjectId(property_to_sell_id)}}})
            #create a sold_property using projection 
            sold_property = mongo_client.PropertyOnSale.find_one({"_id": ObjectId(property_to_sell_id)}, {"_id": 1, "city": 1, "neighbourhood": 1, "price": 1, "thumbnail": 1, "type": 1, "area": 1, "registration_date": 1})
            #add the sell_date to the sold_property
            sold_property["sell_date"] = datetime.now()
            #delete the property from the property_on_sale collection
            result = mongo_client.PropertyOnSale.delete_one({"_id": ObjectId(property_to_sell_id)}) 
            #add the sold_property to the sold_properties of the seller
            result = mongo_client.Seller.update_one({"_id": ObjectId("679a41fa777bc4a7eb04807a")}, {"$push": {"sold_properties": sold_property}})
            return JSONResponse(status_code=200, content={"detail": "Property sold successfully."})
    raise HTTPException(status_code=404, detail="Property not found.")     

@seller_router.get("/", response_model=dict, responses=ResponseModels.GetSellerResponses)
def get_seller(seller_id: str):
    temp_seller = Seller(seller_id=seller_id)
    db_seller = DBSeller(temp_seller)
    response = db_seller.get_seller_by_id()
    if response == 400:
        raise HTTPException(status_code=400, detail="Invalid seller id")
    if response == 404:
        raise HTTPException(status_code=404, detail="Seller not found.")
    return db_seller.seller.model_dump(exclude_none=True,exclude={"seller_id"})

@seller_router.put("/", response_model=ResponseModels.SuccessModel, responses=ResponseModels.UpdateSellerResponses)
def update_seller(seller: UpdateSeller):
    db_seller = DBSeller(Seller(**seller.model_dump()))
    response = db_seller.update_seller_by_id()
    if response == 400:
        raise HTTPException(status_code=400, detail="Invalid seller id")
    if response == 404:
        raise HTTPException(status_code=404, detail="Seller not found.")
    return JSONResponse(status_code=200, content={"detail": "Seller updated successfully."})

# change information of a property on sale for a seller 
@seller_router.put("/methods/change_informations", response_model=ResponseModels.SuccessModel)
def change_informations(new_informations: UpdatePropertyOnSale):
    if not new_informations:
        raise HTTPException(status_code=400, detail="Invalid informations.")
    if new_informations.property_on_sale_id is None:
        raise HTTPException(status_code=400, detail="Property on sale id not specified.")
    try:
        id = ObjectId(new_informations.property_on_sale_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid property on sale id.")
    mongo_client = get_default_mongo_db()
    if mongo_client is None:
        raise HTTPException(status_code=500, detail="Failed to connect to database.")
    #check if the property on sale is the properties_on_sale of the seller
    result = mongo_client.Seller.find_one({"_id": ObjectId("679a41fa777bc4a7eb04807a"), "properties_on_sale._id": id})
    if not result:
        raise HTTPException(status_code=404, detail="Property on sale not found.")
    #retrieve the property on sale from the property_on_sale collection
    property_on_sale_actual = mongo_client.PropertyOnSale.find_one({"_id": id})
    #modify only the informations that are in new_informations and update property_on_sale collection
    new_informations = new_informations.model_dump(exclude_none=True, exclude={"property_on_sale_id"})
    keys = new_informations.keys()
    for key in keys:
        property_on_sale_actual[key] = new_informations[key]
    result = mongo_client.PropertyOnSale.update_one({"_id": id}, {"$set": property_on_sale_actual})
    #update the properties_on_sale of the seller
    property_on_sale_seller={
        "_id": id,
        "city": property_on_sale_actual["city"],
        "neighbourhood": property_on_sale_actual["neighbourhood"],
        "address": property_on_sale_actual["address"],
        "price": property_on_sale_actual["price"],
        "thumbnail": property_on_sale_actual["thumbnail"]
    }
    if "disponibility" in property_on_sale_actual:
        property_on_sale_seller["disponibility"] = property_on_sale_actual["disponibility"]
    result = mongo_client.Seller.update_one({"_id": ObjectId("679a41fa777bc4a7eb04807a"), "properties_on_sale._id": id}, {"$set": {"properties_on_sale.$": property_on_sale_seller}})
            
            


            
    

@seller_router.delete("/", response_model=ResponseModels.SuccessModel, responses=ResponseModels.DeleteSellerResponses)
def delete_seller(seller_id: str):
    temp_seller = Seller(seller_id=seller_id)
    db_seller = DBSeller(temp_seller)
    response = db_seller.delete_seller_by_id()
    if response == 400:
        raise HTTPException(status_code=400, detail="Invalid seller id")
    if response == 404:
        raise HTTPException(status_code=404, detail="Seller not found.")
    return JSONResponse(status_code=200, content={"detail": "Seller deleted successfully."})


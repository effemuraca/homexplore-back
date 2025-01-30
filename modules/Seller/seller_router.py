from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from entities.Seller.seller import Seller
from entities.Seller.db_seller import DBSeller
from modules.Seller.models.seller_models import CreateSeller, UpdateSeller
from modules.Seller.models import response_models as ResponseModels
from bson.objectid import ObjectId


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
    if not property_to_sell_id:
        raise HTTPException(status_code=400, detail="Invalid property id.")
    try:
        id = ObjectId(property_to_sell_id)
    except:
        raise HTTPException(status_code=404, detail="Invalid property id.")
    db_entity= DBSeller(Seller())
    result = db_entity.db_sell_property(id)
    if result == 404:
        raise HTTPException(status_code=404, detail="Property not found.")
    if result == 500:
        raise HTTPException(status_code=500, detail="Failed to sell property.")
    return JSONResponse(status_code=200, content={"detail": "Property sold successfully."})  
    
   

@seller_router.get("/", response_model=Seller, responses=ResponseModels.GetSellerResponses)
def get_seller(seller_id: str):
    temp_seller = Seller(seller_id=seller_id)
    db_seller = DBSeller(temp_seller)
    response = db_seller.get_seller_by_id()
    if response == 400:
        raise HTTPException(status_code=400, detail="Invalid seller id")
    if response == 404:
        raise HTTPException(status_code=404, detail="Seller not found.")
    return db_seller.seller

@seller_router.put("/", response_model=ResponseModels.SuccessModel, responses=ResponseModels.UpdateSellerResponses)
def update_seller(seller: UpdateSeller):
    db_seller = DBSeller(Seller(**seller.model_dump()))
    response = db_seller.update_seller_by_id()
    if response == 400:
        raise HTTPException(status_code=400, detail="Invalid seller id")
    if response == 404:
        raise HTTPException(status_code=404, detail="Seller not found.")
    return JSONResponse(status_code=200, content={"detail": "Seller updated successfully."})

    

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

 
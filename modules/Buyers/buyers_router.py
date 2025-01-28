from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse 
from typing import List
from entities.Buyer.buyer import Buyer  # Removed BuyerInfo
from entities.Buyer.db_buyer import BuyerDB
from modules.Buyers.models import response_models as ResponseModels

buyers_router = APIRouter(prefix="/buyers", tags=["buyers"])

@buyers_router.get("/{buyer_id}", response_model=Buyer, responses=ResponseModels.GetBuyerResponseModelResponses)
def get_buyer(buyer_id: str):
    """
    Retrieves a buyer by id.
    """
    buyer_db = BuyerDB()
    found_buyer = buyer_db.get_buyer_by_id(buyer_id)
    if not found_buyer:
        raise HTTPException(status_code=404, detail="Buyer not found.")
    return found_buyer

@buyers_router.post("/", response_model=ResponseModels.SuccessModel, responses=ResponseModels.CreateBuyerResponseModelResponses)
def create_buyer(buyer: Buyer):  # Changed BuyerInfo to Buyer
    """
    Creates a new buyer.
    """
    if not buyer:
        raise HTTPException(status_code=400, detail="Missing buyer info.")
    if not buyer.is_valid():
        raise HTTPException(status_code=400, detail="Invalid buyer info.")
    
    buyer_db = BuyerDB(Buyer(**buyer.dict()))
    if not buyer_db.create_buyer():
        raise HTTPException(status_code=500, detail="Failed to create buyer.")
    
    return JSONResponse(status_code=201, content={"detail": "Buyer created successfully."})

@buyers_router.put("/{buyer_id}", response_model=Buyer, responses=ResponseModels.UpdateBuyerResponseModelResponses)
def update_buyer(buyer_id: str, buyer: Buyer):  # Changed BuyerInfo to Buyer
    """
    Updates an existing buyer by id.
    """
    if not buyer_id:
        raise HTTPException(status_code=400, detail="Buyer ID is required.")
    
    buyer_db = BuyerDB()
    found_buyer = buyer_db.get_buyer_by_id(buyer_id)
    if not found_buyer:
        raise HTTPException(status_code=404, detail="Buyer not found.")
    
    if not buyer.is_valid():
        raise HTTPException(status_code=400, detail="Invalid buyer info.")
    
    if not buyer_db.update_buyer(buyer):
        raise HTTPException(status_code=500, detail="Failed to update buyer.")
    
    updated_buyer = buyer_db.get_buyer_by_id(buyer_id)
    return updated_buyer

@buyers_router.delete("/{buyer_id}", response_model=ResponseModels.SuccessModel, responses=ResponseModels.DeleteBuyerResponseModelResponses)
def delete_buyer(buyer_id: str):
    """
    Deletes a buyer by id.
    """
    buyer_db = BuyerDB()
    if not buyer_db.delete_buyer_by_id(buyer_id):
        raise HTTPException(status_code=404, detail="Buyer not found or delete failed.")
    
    return JSONResponse(status_code=200, content={"detail": "Buyer deleted successfully."})
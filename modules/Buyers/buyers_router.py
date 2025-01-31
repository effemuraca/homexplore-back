from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse 
from typing import List
from entities.Buyer.buyer import Buyer 
from entities.Buyer.db_buyer import BuyerDB
from modules.Buyers.models.buyer_models import CreateBuyer
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
    return buyer_db.buyer

@buyers_router.post("/", response_model=ResponseModels.CreateBuyerResponseModel, responses=ResponseModels.CreateBuyerResponseModelResponses)
def create_buyer(buyer: CreateBuyer):  # Changed BuyerInfo to Buyer
    """
    Creates a new buyer.
    """
    if not buyer:
        raise HTTPException(status_code=400, detail="Missing buyer info.")
    
    buyer_db = BuyerDB(Buyer(**buyer.dict()))
    result = buyer_db.create_buyer()
    if result == 400:
        raise HTTPException(status_code=result, detail="Invalid buyer info.")
    elif result == 500:
        raise HTTPException(status_code=result, detail="Failed to create buyer.")
    elif result == 201:
        return JSONResponse(status_code=201, content={"detail": "Buyer created successfully.", "buyer_id": buyer_db.buyer.buyer_id})

@buyers_router.put("/", response_model=ResponseModels.SuccessModel, responses=ResponseModels.UpdateBuyerResponseModelResponses)
def update_buyer(buyer: Buyer):  # Changed BuyerInfo to Buyer
    """
    Updates an existing buyer.
    """
    
    buyer_db = BuyerDB()
    result = buyer_db.get_buyer_by_id(buyer.buyer_id)
    if result == 404:
        raise HTTPException(status_code=result, detail="Buyer not found.")
    
    result = buyer_db.update_buyer(buyer)
    if result == 400:
        raise HTTPException(status_code=result, detail="Buyer ID is required.")
    elif result == 404:
        raise HTTPException(status_code=result, detail="Buyer not found.")
    elif result == 500:
        raise HTTPException(status_code=result, detail="Failed to update buyer.")
    elif result == 200:
        return JSONResponse(status_code=result, content={"detail": "Buyer updated successfully."})

@buyers_router.delete("/{buyer_id}", response_model=ResponseModels.SuccessModel, responses=ResponseModels.DeleteBuyerResponseModelResponses)
def delete_buyer(buyer_id: str):
    """
    Deletes a buyer by id.
    """
    buyer_db = BuyerDB()
    result = buyer_db.delete_buyer_by_id(buyer_id)
    if result == 400:
        raise HTTPException(status_code=result, detail="Buyer ID is required.")
    elif result == 404:
        raise HTTPException(status_code=result, detail="Buyer not found.")
    elif result == 200:    
        return JSONResponse(status_code=result, content={"detail": "Buyer deleted successfully."})
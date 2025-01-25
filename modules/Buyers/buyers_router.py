from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
from entities.Buyer.buyer import Buyer
from entities.Buyer.buyer import BuyerInfo
from entities.Buyer.db_buyer import BuyerDB
from modules.Buyers.models import response_models as ResponseModels

buyers_router = APIRouter(prefix="/buyers", tags=["buyers"])

@buyers_router.get("/", response_model=Buyer, responses=ResponseModels.GetBuyerResponseModelResponses)
def get_buyer(buyer_id: str):
    """
    Retrieves a buyer by id.
    """
    buyer_db = BuyerDB(Buyer())
    found_buyer = buyer_db.get_buyer_by_id(buyer_id)
    if not found_buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return found_buyer






@buyers_router.post("/", response_model=Buyer, responses=ResponseModels.CreateBuyerResponseModelResponses)    #response_model=Buyer (return type of the function), responses=ResponseModels.CreateBuyerResponseModelResponses(cose carine nella pagina)
def create_buyer(buyer_info: BuyerInfo):
    """
    Creates a new buyer.
    """
    if not buyer_info.check_buyer_info():
        raise HTTPException(status_code=400, detail="Missing buyer info")
    buyer = Buyer(buyer_info)
    buyer_db = BuyerDB(buyer)
    if not buyer_db.create_buyer():
        raise HTTPException(status_code=400, detail="Failed to create buyer")
    return JSONResponse(status_code=201, content=buyer_db.buyer.dict(exclude_none=True))






@buyers_router.put("/", response_model=Buyer, responses=ResponseModels.UpdateBuyerResponseModelResponses)
def update_buyer(buyer: Buyer):
    """
    Updates an existing buyer by id.
    """
    if not buyer.buyer_id:
        raise HTTPException(status_code=400, detail="Buyer ID is required")
    buyer_db = BuyerDB(buyer)
    if not buyer_db.update_buyer(buyer):
        raise HTTPException(status_code=404, detail="Buyer not found or update failed")
    return {"detail": "Buyer updated"}

@buyers_router.delete("/", response_model=Buyer, responses=ResponseModels.DeleteBuyerResponseModelResponses)
def delete_buyer(buyer_id: str):
    """
    Deletes a buyer by id.
    """
    buyer_db = BuyerDB(Buyer())
    if not buyer_db.delete_buyer_by_id(buyer_id):
        raise HTTPException(status_code=404, detail="Buyer not found or delete failed")
    return {"detail": "Buyer deleted"}
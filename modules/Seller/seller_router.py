from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from entities.Seller.seller import Seller
from entities.Seller.db_seller import DBSeller
from modules.Seller.models.seller_models import CreateSeller, UpdateSeller
from modules.Seller.models import response_models as ResponseModels

seller_router = APIRouter(prefix="/sellers", tags=["Sellers"])

@seller_router.post("/", response_model=ResponseModels.CreateSellerResponseModel, responses=ResponseModels.CreateSellerResponses)
def create_seller(seller: CreateSeller):
    db_seller = DBSeller(Seller(**seller.model_dump()))
    response = db_seller.create_seller()
    if response == 400:
        raise HTTPException(status_code=400, detail="Invalid seller information.")
    if response == 500:
        raise HTTPException(status_code=500, detail="Failed to create seller.")
    return JSONResponse(status_code=201, content={"detail": "Seller created successfully.", "seller_id": db_seller.seller.seller_id})

@seller_router.get("/", response_model=ResponseModels.SellerResponseModel, responses=ResponseModels.GetSellerResponses)
def get_seller(seller_id: str):
    temp_seller = Seller(seller_id=seller_id)
    db_seller = DBSeller(temp_seller)
    response = db_seller.get_seller_by_id()
    if response == 400:
        raise HTTPException(status_code=400, detail="Invalid seller id or seller not found.")
    return db_seller.seller

@seller_router.put("/", response_model=ResponseModels.SuccessModel, responses=ResponseModels.UpdateSellerResponses)
def update_seller(seller: UpdateSeller):
    db_seller = DBSeller(Seller(**seller.model_dump()))
    response = db_seller.update_seller_by_id()
    if response == 400:
        raise HTTPException(status_code=400, detail="Invalid seller id or seller not found.")
    return JSONResponse(status_code=200, content={"detail": "Seller updated successfully."})

@seller_router.delete("/", response_model=ResponseModels.SuccessModel, responses=ResponseModels.DeleteSellerResponses)
def delete_seller(seller_id: str):
    temp_seller = Seller(seller_id=seller_id)
    db_seller = DBSeller(temp_seller)
    response = db_seller.delete_seller_by_id()
    if response == 400:
        raise HTTPException(status_code=400, detail="Invalid seller id or seller not found.")
    return JSONResponse(status_code=200, content={"detail": "Seller deleted successfully."})
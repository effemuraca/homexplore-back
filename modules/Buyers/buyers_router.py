from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from entities.Buyer.buyer import Buyer, FavouriteProperty
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
    result = buyer_db.get_contact_info(buyer_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="Buyer not found.")
    elif result == 400:
        raise HTTPException(status_code=400, detail="Invalid buyer ID.")
    elif result == 500:
        raise HTTPException(status_code=500, detail="Internal server error.")
    return buyer_db.buyer

@buyers_router.post("/", response_model=ResponseModels.CreateBuyerResponseModel, responses=ResponseModels.CreateBuyerResponseModelResponses)
def create_buyer(buyer: CreateBuyer):
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
def update_buyer(buyer: Buyer):
    """
    Updates an existing buyer.
    """
    buyer_db = BuyerDB()
    result = buyer_db.get_contact_info(buyer.buyer_id)
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

@buyers_router.get("/{buyer_id}/favorites", response_model=List[FavouriteProperty], responses=ResponseModels.GetFavoritesResponseModelResponses)
def get_favorites(buyer_id: str):
    """
    Retrieves the favorite properties of a buyer by id.
    """
    buyer_db = BuyerDB()
    favorites = buyer_db.get_favorites(buyer_id)
    if favorites is None:
        raise HTTPException(status_code=404, detail="Favorites not found.")
    return favorites

@buyers_router.post("/{buyer_id}/favorites", response_model=ResponseModels.SuccessModel, responses=ResponseModels.AddFavoriteResponseModelResponses)
def add_favorite(buyer_id: str, favorite: FavouriteProperty):
    """
    Adds a favorite property for a buyer.
    """
    buyer_db = BuyerDB()
    result = buyer_db.add_favorite(buyer_id, favorite)
    if result == 400:
        raise HTTPException(status_code=result, detail="Invalid input.")
    elif result == 500:
        raise HTTPException(status_code=result, detail="Failed to add favorite.")
    elif result == 200:
        return JSONResponse(status_code=result, content={"detail": "Favorite added successfully."})

@buyers_router.delete("/{buyer_id}/favorites/{property_id}", response_model=ResponseModels.SuccessModel, responses=ResponseModels.DeleteFavoriteResponseModelResponses)
def delete_favorite(buyer_id: str, property_id: str):
    """
    Deletes a favorite property for a buyer.
    """
    buyer_db = BuyerDB()
    result = buyer_db.delete_favorite(buyer_id, property_id)
    if result == 400:
        raise HTTPException(status_code=result, detail="Invalid input.")
    elif result == 500:
        raise HTTPException(status_code=result, detail="Failed to delete favorite.")
    elif result == 200:
        return JSONResponse(status_code=result, content={"detail": "Favorite deleted successfully."})

@buyers_router.put("/{buyer_id}/favorites/{property_id}", response_model=ResponseModels.SuccessModel, responses=ResponseModels.UpdateFavoriteResponseModelResponses)
def update_favorite(buyer_id: str, property_id: str, favorite: FavouriteProperty):
    """
    Updates a favorite property for a buyer.
    """
    buyer_db = BuyerDB()
    result = buyer_db.update_favorite(buyer_id, property_id, favorite.dict())
    if result == 400:
        raise HTTPException(status_code=result, detail="Invalid input.")
    elif result == 500:
        raise HTTPException(status_code=result, detail="Failed to update favorite.")
    elif result == 200:
        return JSONResponse(status_code=result, content={"detail": "Favorite updated successfully."})
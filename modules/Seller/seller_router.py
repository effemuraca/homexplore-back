from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from entities.MongoDB.Seller.seller import Seller
from entities.MongoDB.Seller.db_seller import DBSeller
from modules.Seller.models.seller_models import CreateSeller, UpdateSeller
from modules.Seller.models import response_models as ResponseModels
from entities.Redis.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS
from entities.Redis.ReservationsSeller.db_reservations_seller import ReservationsSellerDB
from modules.Seller.models import response_models as ResponseModels
from modules.Seller.models.seller_models import CreateReservationSeller, UpdateReservationSeller, UpdateEntireReservationSeller
from entities.MongoDB.PropertyOnSale.property_on_sale import PropertyOnSale
from entities.MongoDB.PropertyOnSale.db_property_on_sale import PropertyOnSaleDB
from modules.Seller.models import response_models as ResponseModels
from modules.Seller.models.seller_models import CreatePropertyOnSale, UpdatePropertyOnSale
from typing import List, Optional

from bson.objectid import ObjectId

seller_router = APIRouter(prefix="/seller", tags=["Seller"])


#Seller

# @seller_router.post("/", response_model=ResponseModels.CreateSellerResponseModel, responses=ResponseModels.CreateSellerResponses)
# def create_seller(seller: CreateSeller):
#     db_seller = DBSeller(Seller(**seller.model_dump()))
#     response = db_seller.create_seller()
#     if response == 400:
#         raise HTTPException(status_code=400, detail="Invalid seller information.")
#     if response == 500:
#         raise HTTPException(status_code=500, detail="Failed to create seller.")
#     return JSONResponse(status_code=201, content={"detail": "Seller created successfully.", "seller_id": db_seller.seller.seller_id})

# sell a property (move it from properties_on_sale to sold_properties of the seller & delete it from the property_on_sale collection)
@seller_router.post("/sell_property_on_sale", response_model=ResponseModels.SuccessModel)
def sell_property(seller_id: str, property_to_sell_id: str):
    if not property_to_sell_id or not seller_id:
        raise HTTPException(status_code=400, detail="Invalid property id or seller id.")
    try:
        property_id = ObjectId(property_to_sell_id)
        seller_id = ObjectId(seller_id)
    except:
        raise HTTPException(status_code=404, detail="Invalid property id or seller id.")
    db_entity = DBSeller(Seller())
    result = db_entity.db_sell_property(seller_id, property_id)
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

@seller_router.get("/{seller_id}/sold_properties", response_model=Seller, responses=ResponseModels.GetSoldPropertiesByPriceDescResponses)
def get_sold_properties_by_price_desc(seller_id: str):
    db_seller = DBSeller()
    result = db_seller.get_sold_properties_by_price_desc(seller_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="Seller not found.")
    if result == 500:
        raise HTTPException(status_code=500, detail="Failed to retrieve sold properties.")
    return db_seller.seller


# Properties on sale

@seller_router.post("/properties_on_sale", response_model=ResponseModels.CreatePropertyOnSaleResponseModel, responses=ResponseModels.CreatePropertyOnSaleResponses)
def create_property_on_sale(property_on_sale: CreatePropertyOnSale):
    property_on_sale = PropertyOnSale(**property_on_sale.model_dump())
    db_property_on_sale = PropertyOnSaleDB(property_on_sale)
    response = db_property_on_sale.create_property_on_sale()
    if response == 400:
        raise HTTPException(status_code=response, detail="Invalid property information.")
    if response == 500:
        raise HTTPException(status_code=response, detail="Failed to create property.")
    return JSONResponse(status_code=201, content={"detail": "Property created successfully.", "property_id": property_on_sale.property_on_sale_id})

@seller_router.get("/properties_on_sale", response_model=ResponseModels.PropertyOnSale, responses=ResponseModels.GetPropertiesOnSaleResponses)
def get_properties_on_sale(property_on_sale_id: str):
    db_property_on_sale = PropertyOnSaleDB(PropertyOnSale())
    response = db_property_on_sale.get_property_on_sale_by_id(property_on_sale_id)
    if response == 400:
        raise HTTPException(status_code=response, detail="Invalid property id.")
    if response == 404:
        raise HTTPException(status_code=response, detail="Property not found.")
    return db_property_on_sale.property_on_sale

@seller_router.delete("/properties_on_sale", response_model=ResponseModels.SuccessModel, responses=ResponseModels.DeletePropertyOnSaleResponses)
def delete_property_on_sale(property_on_sale_id: str):
    db_property_on_sale = PropertyOnSaleDB(PropertyOnSale())
    response = db_property_on_sale.delete_property_on_sale_by_id(property_on_sale_id)
    if response == 400:
        raise HTTPException(status_code=response, detail="Invalid property id.")
    if response == 404:
        raise HTTPException(status_code=response, detail="Property not found.")
    return JSONResponse(status_code=200, content={"detail": "Property deleted successfully."})

@seller_router.put("/properties_on_sale", response_model=ResponseModels.SuccessModel, responses=ResponseModels.UpdatePropertyOnSaleResponses)
def update_property_on_sale(property_on_sale: UpdatePropertyOnSale):
    property_on_sale = PropertyOnSale(**property_on_sale.model_dump())
    db_property_on_sale = PropertyOnSaleDB(property_on_sale)
    response = db_property_on_sale.update_property_on_sale()
    if response == 400:
        raise HTTPException(status_code=response, detail="Invalid property id.")
    if response == 404:
        raise HTTPException(status_code=response, detail="Property not found.")
    return JSONResponse(status_code=200, content={"detail": "Property updated successfully."})

@seller_router.get("/properties_on_sale/search", response_model=List[PropertyOnSale], responses=ResponseModels.GetFilteredPropertiesOnSaleResponses)
def filtered_search(
    city: Optional[str] = None,
    max_price: Optional[int] = None,
    neighbourhood: Optional[str] = None,
    type: Optional[str] = None,
    area: Optional[int] = None,
    min_bed_number: Optional[int] = None,
    min_bath_number: Optional[int] = None
):
    db_property_on_sale = PropertyOnSaleDB(PropertyOnSale())
    result_code = db_property_on_sale.filtered_search(
        city=city if city else "",
        max_price=max_price if max_price is not None else 0,
        neighbourhood=neighbourhood if neighbourhood else "",
        type=type if type else "",
        area=area if area is not None else 0,
        min_bed_number=min_bed_number if min_bed_number is not None else 0,
        min_bath_number=min_bath_number if min_bath_number is not None else 0
    )
    if result_code == 500:
        raise HTTPException(status_code=500, detail="Internal server error.")
    return db_property_on_sale.property_on_sale


@seller_router.get("/properties_on_sale/get_random", response_model=List[PropertyOnSale], responses=ResponseModels.GetRandomPropertiesOnSaleResponses)
def get_10_random_properties():
    db_property_on_sale = PropertyOnSaleDB(PropertyOnSale())
    result_code = db_property_on_sale.get_10_random_properties()
    if result_code == 500:
        raise HTTPException(status_code=500, detail="Internal server error.")
    return db_property_on_sale.property_on_sale

# ReservationsSeller

@seller_router.post(
    "/reservations",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.CreateReservationSellerResponseModelResponses
)
def create_reservation_seller(reservations_seller_info: CreateReservationSeller):
    reservations_seller = ReservationsSeller(
        property_on_sale_id=reservations_seller_info.property_on_sale_id,
        reservations=[ReservationS(
            buyer_id=reservations_seller_info.buyer_id,
            full_name=reservations_seller_info.full_name,
            email=reservations_seller_info.email,
            phone=reservations_seller_info.phone
        )],
        # Imposto total_reservations iniziale a 1 per registrare almeno una prenotazione
        total_reservations=1,
        area=reservations_seller_info.area
    )
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    status = reservations_seller_db.create_reservation_seller(reservations_seller_info.day, reservations_seller_info.time)
    if status == 200:
        return ResponseModels.SuccessModel(detail="Reservation created successfully.")
    elif status == 409:
        raise HTTPException(status_code=409, detail="Reservation already exists.")
    else:
        raise HTTPException(status_code=500, detail="Failed to create reservation.")
    
@seller_router.get(
    "/reservations",
    response_model=ReservationsSeller,
    responses=ResponseModels.GetReservationsSellerResponseModelResponses
)
def get_reservations_seller(property_on_sale_id: str):
    reservations_seller = ReservationsSeller(property_on_sale_id=property_on_sale_id)
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    status = reservations_seller_db.get_reservation_seller()
    if status == 404:
        raise HTTPException(status_code=404, detail="No reservations found.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to fetch reservations.")
    return reservations_seller_db.reservations_seller

@seller_router.put(
    "/reservations",
    response_model=ReservationsSeller,
    responses=ResponseModels.UpdateReservationsSellerResponseModelResponses
)
def update_reservations_seller(reservations_seller_info: UpdateReservationSeller):
    if not reservations_seller_info.buyer_id:
        raise HTTPException(status_code=400, detail="Buyer ID is required for update.")
    reservations_seller = ReservationsSeller(
        property_on_sale_id=reservations_seller_info.property_on_sale_id,
        reservations=[ReservationS(
            buyer_id=reservations_seller_info.buyer_id,
            full_name=reservations_seller_info.full_name,
            email=reservations_seller_info.email,
            phone=reservations_seller_info.phone
        )]
    )
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    status = reservations_seller_db.update_reservation_seller(reservations_seller_info.buyer_id, reservations_seller_info.dict(exclude_unset=True))
    if status == 404:
        raise HTTPException(status_code=404, detail="Reservation not found.")
    if status == 400:
        raise HTTPException(status_code=400, detail="Invalid input provided.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to update reservation.")
    reservations_seller_db.get_reservation_seller()
    return reservations_seller_db.reservations_seller

@seller_router.put(
    "/reservations/bulk",
    response_model=ReservationsSeller,
    responses=ResponseModels.UpdateReservationsSellerResponseModelResponses
)
def update_entire_reservations_seller(reservations_seller_info: UpdateEntireReservationSeller):
    reservations_seller = ReservationsSeller(property_on_sale_id=reservations_seller_info.property_on_sale_id)
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    status = reservations_seller_db.update_entire_reservation_seller(area=reservations_seller_info.area)
    if status == 400:
        raise HTTPException(status_code=400, detail="Maximum reservations exceeded.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to update entire reservations.")
    return ResponseModels.SuccessModel(detail="Entire reservation updated successfully.")

@seller_router.delete(
    "/reservations",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.DeleteReservationsSellerResponseModelResponses
)
def delete_reservations_seller(property_on_sale_id: str):
    reservations_seller = ReservationsSeller(property_on_sale_id=property_on_sale_id)
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    status = reservations_seller_db.delete_entire_reservation_seller()
    if status == 404:
        raise HTTPException(status_code=404, detail="Reservation not found or delete failed.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to delete reservation.")
    
@seller_router.delete(
    "/reservations/{buyer_id}/{property_on_sale_id}",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.DeleteReservationsSellerResponseModelResponses
)
def delete_reservation_seller_by_buyer_id(buyer_id: str, property_on_sale_id: str):
    reservations_seller = ReservationsSeller(
        property_on_sale_id=property_on_sale_id,
        reservations=[ReservationS(buyer_id=buyer_id)]
    )
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    status = reservations_seller_db.delete_reservation_seller_by_buyer_id(buyer_id)
    if status == 404:
        raise HTTPException(status_code=404, detail="Reservation not found.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to delete reservation.")
    return JSONResponse(status_code=200, content={"detail": "Seller reservation deleted successfully."})
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from entities.PropertyOnSale.property_on_sale import Disponibility

class SoldProperty(BaseModel):
    sold_property_id: Optional[str] = None
    city: Optional[str] = None
    neighbourhood: Optional[str] = None
    price: Optional[int] = None
    thumbnail: Optional[str] = None
    type: Optional[str] = None
    area: Optional[int] = None
    registration_date: Optional[datetime] = None
    sell_date: Optional[datetime] = None

class SellerPropertyOnSale(BaseModel):
    property_on_sale_id: Optional[str] = None
    city: Optional[str] = None
    neighbourhood: Optional[str] = None
    address: Optional[str] = None
    price: Optional[int] = None
    thumbnail: Optional[str] = None
    disponibility: Optional[Disponibility] = None

class Seller(BaseModel):
    seller_id: Optional[str] = None
    agency_name: Optional[str] = None
    email: Optional[str]=None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    property_on_sale: Optional[List[SellerPropertyOnSale]] = None
    sold_property: Optional[List[SoldProperty]] = None

from pydantic import BaseModel, validator, EmailStr
from typing import List, Optional
from datetime import datetime
from entities.MongoDB.PropertyOnSale.property_on_sale import Disponibility
from bson import ObjectId

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
    
    @validator('sold_property_id')
    def check_object_id(cls, v: str) -> str:
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId string')
        return v

class SellerPropertyOnSale(BaseModel):
    property_on_sale_id: Optional[str] = None
    city: Optional[str] = None
    neighbourhood: Optional[str] = None
    address: Optional[str] = None
    price: Optional[int] = None
    thumbnail: Optional[str] = None
    disponibility: Optional[Disponibility] = None
    
    @validator('property_on_sale_id')
    def check_object_id(cls, v: str) -> str:
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId string')
        return v

class Seller(BaseModel):
    seller_id: Optional[str] = None
    agency_name: Optional[str] = None
    email: Optional[EmailStr]=None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    properties_on_sale: Optional[List[SellerPropertyOnSale]] = None
    sold_properties: Optional[List[SoldProperty]] = None
    
    @validator('seller_id')
    def check_object_id(cls, v: str) -> str:
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId string')
        return v

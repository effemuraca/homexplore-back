import re
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from bson.objectid import ObjectId
import math

class FavouriteProperty(BaseModel):
    property_on_sale_id: str
    thumbnail: str
    address: str
    price: int
    area: int

    @field_validator('property_on_sale_id')
    def check_object_id(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError('Invalid ObjectId string')
        return value
    
    @field_validator('thumbnail')
    def validate_thumbnail(cls, value):
        if not re.match(r'^https?://.*\.(?:png|jpg|jpeg|gif)$', value):
            raise ValueError('Invalid URL format.')
        return value
    
    @field_validator('price')
    def validate_price(cls, value):
        if value < 0:
            raise ValueError('Price must be positive.')
        return value

    @field_validator('area', mode='before')
    def parse_nan_to_zero(cls, value):
        if isinstance(value, float) and math.isnan(value):
            return 0
        return value
    
    @field_validator('area')
    def validate_area(cls, value):
        if value < 0:
            raise ValueError('Area must be positive.')
        return value




class Buyer(BaseModel):
    buyer_id: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    favourites: Optional[list[FavouriteProperty]] = None
    
    @field_validator('buyer_id')
    def check_object_id(cls, v: str) -> str:
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId string')
        return v
    
    



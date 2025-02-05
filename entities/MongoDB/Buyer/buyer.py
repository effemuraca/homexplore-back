import logging
import re
from pydantic import BaseModel, Field, EmailStr, validator, field_validator
from typing import Optional
from bson.objectid import ObjectId

# Configura il logger
logger = logging.getLogger(__name__)

class FavouriteProperty(BaseModel):
    property_id: str
    thumbnail: str
    address: str
    price: int
    area: int

    @field_validator('property_id')
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
        if value <= 0:
            raise ValueError('Price must be greater than zero.')
        return value
    
    @field_validator('area')
    def validate_area(cls, value):
        if value <= 0:
            raise ValueError('Area must be greater than zero.')
        return value
    
    @field_validator('address')
    def check_address(cls, v: str) -> str:
        if not re.match(r'^[0-9]+ .+$', v):
            raise ValueError('Invalid address format')
        return v



class Buyer(BaseModel):
    buyer_id: str = Field(None, example="60d5ec49f8d2e30b8c8b4567")
    password: Optional[str] = Field(None, example="SecureP@ssw0rd")
    email: Optional[EmailStr] = Field(None, example="john.doe@example.com")
    phone_number: Optional[str] = Field(None, example="+1 1234567890")
    name: Optional[str] = Field(None, example="John")
    surname: Optional[str] = Field(None, example="Doe")
    favourites: Optional[list[FavouriteProperty]] = Field(None, example=[{
        "property_id": "1",
        "thumbnail": "https://www.example.com/image.jpg",
        "address": "1234 Example St.",
        "price": 100000,
        "area": 100
    }])
    
    @validator('buyer_id')
    def check_object_id(cls, v: str) -> str:
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId string')
        return v
    
    @validator('phone_number')
    def validate_phone_number(cls, value):
        if value:
            phone_pattern = re.compile(r'^\+\d{1,3}\s?\d{7,14}$')
            if not phone_pattern.match(value):
                raise ValueError('Invalid phone number format.')
        return value


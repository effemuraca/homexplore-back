import logging
import re
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional

# Configura il logger
logger = logging.getLogger(__name__)

class FavouriteProperty(BaseModel):
    property_id: str
    thumbnail: str
    address: str
    price: int
    area: int

class Buyer(BaseModel):
    buyer_id: str = Field(None, example="60d5ec49f8d2e30b8c8b4567")
    password: Optional[str] = Field(None, example="SecureP@ssw0rd")
    email: Optional[EmailStr] = Field(None, example="john.doe@example.com")
    phone_number: Optional[str] = Field(None, example="+1 1234567890")
    name: Optional[str] = Field(None, example="John")
    surname: Optional[str] = Field(None, example="Doe")
    age: Optional[int] = Field(None, example=30)  #campo opzionale
    favorites: Optional[list[FavouriteProperty]] = Field(None, example=[{
        "property_id": "1",
        "thumbnail": "https://www.example.com/image.jpg",
        "address": "1234 Example St.",
        "price": 100000,
        "area": 100
    }])
    
    @validator('phone_number')
    def validate_phone_number(cls, value):
        if value:
            phone_pattern = re.compile(r'^\+\d{1,3}\s?\d{7,14}$')
            if not phone_pattern.match(value):
                raise ValueError('Invalid phone number format.')
        return value

from pydantic import BaseModel, Field
from typing import Optional, List
from pydantic.networks import EmailStr


class FavouriteProperty(BaseModel):
    property_id: str
    thumbnail: str
    address: str
    price: int
    area: int

class CreateBuyer(BaseModel):
    password: str = Field(None, example="SecureP@ssw0rd")
    email: EmailStr = Field(None, example="john.doe@example.com")
    phone_number: Optional[str] = Field(None, example="+1 1234567890")
    name: str = Field(None, example="John")
    surname: str = Field(None, example="Doe")
    age: Optional[int] = Field(None, example=30)  #campo opzionale
    favorites: Optional[list[FavouriteProperty]] = Field(None, example=[{
        "property_id": "1",
        "thumbnail": "https://www.example.com/image.jpg",
        "address": "1234 Example St.",
        "price": 100000,
        "area": 100
    }])
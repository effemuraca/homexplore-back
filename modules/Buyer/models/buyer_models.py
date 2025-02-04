from pydantic import BaseModel, Field
from typing import Optional
from pydantic.networks import EmailStr

class FavouriteProperty(BaseModel):
    property_id: str
    thumbnail: str
    address: str
    price: int
    area: int

class CreateBuyer(BaseModel):
    email: EmailStr = Field(None, example="john.doe@example.com")
    password: str = Field(None, example="SecureP@ssw0rd")
    name: str = Field(None, example="John")
    surname: str = Field(None, example="Doe")
    phone_number: Optional[str] = Field(None, example="+1 1234567890")
    

class CreateReservationBuyer(BaseModel):
    property_on_sale_id: str = Field(example="615c44fdf641be001f0c1111")
    buyer_id: str = Field(example="615c44fdf641be001f0c1111")
    date: str = Field(example="2021-09-01")
    time: str = Field(example="10:00")
    thumbnail: str = Field(example="https://www.example.com/image")
    address: str = Field(example="1234 Example St.")

class UpdateReservationBuyer(BaseModel):
    property_on_sale_id: str = Field(example="615c44fdf641be001f0c1111")
    buyer_id: str = Field(example="615c44fdf641be001f0c1111")
    date: str = Field(example="2021-09-01")
    time: str = Field(example="10:00")
    thumbnail: str = Field(example="https://www.example.com/image")
    address: str = Field(example="1234 Example St.")


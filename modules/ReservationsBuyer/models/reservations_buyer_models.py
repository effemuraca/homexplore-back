from pydantic import BaseModel, Field
from typing import Optional


class CreateReservationBuyer(BaseModel):
    property_id: str = Field(example="615c44fdf641be001f0c1111")
    buyer_id: str = Field(example="615c44fdf641be001f0c1111")
    date: str = Field(example="2021-09-01")
    time: str = Field(example="10:00")
    thumbnail: str = Field(example="https://www.example.com/image")
    address: str = Field(example="1234 Example St.")

                           

class UpdateReservationBuyer(BaseModel):
    property_id: str = Field(example="615c44fdf641be001f0c1111")
    buyer_id: str = Field(example="615c44fdf641be001f0c1111")
    date: str = Field(example="2021-09-01")
    time: str = Field(example="10:00")
    thumbnail: str = Field(example="https://www.example.com/image")
    address: str = Field(example="1234 Example St.")


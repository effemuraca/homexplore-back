from pydantic import BaseModel, Field
from typing import Optional, List

class ReservationB(BaseModel):
    property_id: Optional[int] = Field(None, example=1)
    date: Optional[str] = Field(None, example="2021-09-01")
    time: Optional[str] = Field(None, example="10:00")
    thumbnail: Optional[str] = Field(None, example="https://www.example.com/image.jpg")
    address: Optional[str] = Field(None, example="1234 Example St.")

class ReservationsBuyer(BaseModel):
    buyer_id: Optional[int] = Field(None, example=1)
    reservations: Optional[List[ReservationB]] = None
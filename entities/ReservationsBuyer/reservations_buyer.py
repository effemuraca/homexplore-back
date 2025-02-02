from pydantic import BaseModel, Field, validator
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

class ReservationB(BaseModel):
    property_on_sale_id: Optional[str] = Field(None, example=1)
    date: Optional[str] = Field(None, example="2021-09-01")
    time: Optional[str] = Field(None, example="10:00")
    thumbnail: Optional[str] = Field(None, example="https://www.example.com/image.jpg")
    address: Optional[str] = Field(None, example="1234 Example St.")
    
    @validator('property_on_sale_id')
    def check_object_id(cls, v: str) -> str:
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId string')
        return v
    
    def check_reservation_expired(self) -> bool:
        """
        Checks if the reservation has expired.
        """
        # Check if the reservation date is in the past
        return datetime.strptime(self.date, "%Y-%m-%d") < datetime.now()
    

class ReservationsBuyer(BaseModel):
    buyer_id: Optional[str] = Field(None, example=1)
    reservations: Optional[List[ReservationB]] = None
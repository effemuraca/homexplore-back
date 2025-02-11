from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from bson import ObjectId
from datetime import datetime
import re

class ReservationB(BaseModel):
    property_on_sale_id: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    thumbnail: Optional[str] = None
    address: Optional[str] = None
    
    @field_validator('property_on_sale_id')
    def check_object_id(cls, v: str) -> str:
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId string')
        return v
    
    @field_validator('date')
    def validate_date(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError('Invalid date format.')
        return v
    
    @field_validator('time')
    def validate_time(cls, v):
        pattern = r"^(0?[1-9]|1[0-2]):[0-5][0-9] (AM|PM) - (0?[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$"
        if not re.match(pattern, v):
            raise ValueError('Invalid time')
        return v
    
    @field_validator('thumbnail')
    def validate_thumbnail(cls, v: str) -> str:
        if not re.match(r'^https?://.*\.(?:png|jpg|jpeg|gif)$', v):
            raise ValueError('Invalid URL format.')
        return v
    
    def check_reservation_expired(self) -> bool:
        """
        Checks if the reservation has expired (date is in the past)

        Returns:
            bool: True if the reservation has expired, False otherwise
        """
        return datetime.strptime(self.date, "%Y-%m-%d") < datetime.now()
    

class ReservationsBuyer(BaseModel):
    buyer_id: Optional[str] = None
    reservations: Optional[List[ReservationB]] = None
    
    @field_validator('buyer_id')
    def check_object_id(cls, v: str) -> str:
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId string')
        return v
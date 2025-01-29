from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional, Dict, Any, Set
from datetime import datetime
import re


class Disponibility(BaseModel):
    day: str = Field(example="Monday")
    time: str = Field(example="10:00-11:00 AM")
    max_attendees: int = Field(example=5)

    @validator("day")
    def validate_day(cls, value):
        valid_days = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}
        if value not in valid_days:
            raise ValueError("Invalid day. Must be one of: " + ", ".join(valid_days))
        return value

    @validator("time")
    def validate_time(cls, value):
        time_pattern = re.compile(r"^(0[1-9]|1[0-2]):[0-5][0-9]-(0[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$")
        if not time_pattern.match(value):
            raise ValueError("Invalid time format. Expected format: HH:MM-HH:MM AM/PM")
        return value

class PropertyOnSale(BaseModel):
    property_on_sale_id: Optional[str] = None
    city: Optional[str] = None
    neighbourhood: Optional[str] = None
    address: Optional[str] = None
    price: Optional[int] = None
    thumbnail: Optional[str] = None
    type: Optional[str] = None
    area: Optional[int] = None
    registration_date: Optional[datetime] = None
    bed_number: Optional[int] = None
    bath_number: Optional[int] = None
    description: Optional[str] = None
    photos: Optional[List[str]] = None
    disponibility: Optional[Disponibility] = None
    
    

    
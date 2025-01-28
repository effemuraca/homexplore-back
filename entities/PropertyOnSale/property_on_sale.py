from pydantic import BaseModel, Field, EmailStr, Date
from typing import List, Optional, Dict, Any, Set
import re


class Disponibility(BaseModel):
    day: str = Field(example="Monday")
    time: str = Field(example="10:00-11:00 AM")
    max_attendees: int = Field(example=5)

    #Valide day field and time field
    def validate_day_time(self):
        if self.day not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            return False
        time_pattern = re.compile(r"^(0[1-9]|1[0-2]):[0-5][0-9]-(0[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$")
        if not time_pattern.match(self.time):
            return False
        return True

class PropertyOnSale(BaseModel):
    property_on_sale_id: Optional[str] = None
    city: Optional[str] = None
    neighbourhood: Optional[str] = None
    address: Optional[str] = None
    price: Optional[int] = None
    thumbnail: Optional[str] = None
    type: Optional[str] = None
    area: Optional[int] = None
    registration_date: Optional[Date] = None
    bed_number: Optional[int] = None
    bath_number: Optional[int] = None
    description: Optional[str] = None
    photos: Optional[List[str]] = None
    disponibility: Optional[Disponibility] = None


    #Control that the minimum info is present for inserting a property
    def check_min_info(self):
        if not self.city or not self.neighbourhood or not self.address or not self.price or not self.thumbnail or not self.type or not self.area:
            return False
        if self.disponibility and not self.disponibility.validate_day_time():
            return False
        if self.type not in ["condo", "house", "apartment", "townhouse"]:
            return False
        return True

    
    

    
from pydantic import BaseModel, field_validator
from typing import List, Optional, Dict, Any, Set
from datetime import datetime
from bson import ObjectId
import re



class Disponibility(BaseModel):
    day: Optional[str] = None
    time: Optional[str] = None
    max_attendees: Optional[int] = None
    
    @field_validator('day')
    def validate_day(cls, v):
        if v not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            raise ValueError('Invalid day')
        return v
    
    @field_validator('time')
    def validate_time(cls, v):
        pattern = r"^(0?[1-9]|1[0-2]):[0-5][0-9] (AM|PM) - (0?[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$"
        if not re.match(pattern, v):
            raise ValueError('Invalid time')
        return v
    
    @field_validator('max_attendees')
    def validate_max_attendees(cls, v):
        if v < 1 or v > 1000:
            raise ValueError('Invalid max_attendees')
        return v


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
 
    @field_validator('property_on_sale_id')
    def check_object_id(cls, v: str) -> str:
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId string')
        return v
    
    @field_validator('thumbnail')
    def validate_thumbnail(cls, v: str) -> str:
        if not re.match(r'^https?://.*\.(?:png|jpg|jpeg|gif)$', v):
            raise ValueError('Invalid URL format.')
        return v
    
    @field_validator('price')
    def validate_price(cls, v: int) -> int:
        if v < 0:
            raise ValueError('Price must be positive.')
        return v
    
    @field_validator('area')
    def validate_area(cls, v: int) -> int:
        if v < 0:
            raise ValueError('Area must be positive.')
        return v
    
    @field_validator("photos")
    def validate_photos(cls, v):
        for photo in v:
            if not re.match(r'^https?://.*\.(?:png|jpg|jpeg|gif)$', photo):
                raise ValueError("Invalid URL format")
        return v
    
    def convert_to_seller_property(self) -> Dict[str, Any]:
        """
        Converts the PropertyOnSale object to a dictionary with the same fields
        """
        data = {
            "_id": ObjectId(self.property_on_sale_id),
            "city": self.city,
            "neighbourhood": self.neighbourhood,
            "address": self.address,
            "price": self.price,
            "thumbnail": self.thumbnail
        }
        if self.disponibility:
            data["disponibility"] = self.disponibility.model_dump()
        return data
    

    
    
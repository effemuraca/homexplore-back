from pydantic import BaseModel, validator
from typing import List, Optional, Dict, Any, Set
from datetime import datetime
from bson import ObjectId



class Disponibility(BaseModel):
    day: Optional[str] = None
    time: Optional[str] = None
    max_attendees: Optional[int] = None


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
    
    @validator('property_on_sale_id')
    def check_object_id(cls, v: str) -> str:
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId string')
        return v
    
    

    
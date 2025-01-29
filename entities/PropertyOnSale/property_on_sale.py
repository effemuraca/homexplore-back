from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Set
from datetime import datetime



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
    
    

    
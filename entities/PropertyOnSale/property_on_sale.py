from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any, Set
from datetime import datetime


class Disponibility(BaseModel):
    date: Optional[str] = Field(None, example="Monday")
    time: Optional[str] = Field(None, example="10:00-11:00 AM")
    max_attendees: Optional[int] = Field(None, example=5)

class PropertyOnSale(BaseModel):
    property_on_sale_id : Optional[str] = Field(None, example="unique_house_identifier")
    city: Optional[str] = Field(None, example="New York")
    neighbourhood: Optional[str] = Field(None, example="Bronx")
    address: Optional[str] = Field(None, example="123 Main St")
    price: Optional[float] = Field(None, example=270000)
    thumbnail: Optional[str] = Field(None, example="http://example.com/photo.jpg")
    type: Optional[str] = Field(None, example="condo")
    area: Optional[int] = Field(None, example=100)
    registration_date: Optional[datetime] = Field(None, example="2020-05-11T22:00:00Z")
    bed_number: Optional[int] = Field(None, example=3) #Optional field
    bath_number: Optional[int] = Field(None, example=2) #Optional field
    description: Optional[str] = Field(None, example="Beautiful home") #Optional field
    photos: Optional[List[str]] = Field(None, example=["http://example.com/photo1.jpg"]) #Optional field
    disponibility: Optional[Disponibility] = None   #Optional field


    #Control that the minimum info is present
    def check_min_info(self):
        if not all([self.city, self.neighbourhood, self.address, self.price, self.thumbnail, self.type, self.area]):
            return False
        return True

    
    

    
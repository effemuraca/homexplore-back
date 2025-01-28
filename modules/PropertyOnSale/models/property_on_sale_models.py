from pydantic import BaseModel, Field, EmailStr
from entities.PropertyOnSale.property_on_sale import Disponibility
from typing import List, Optional

class CreatePropertyOnSale(BaseModel):
    city: str = Field(example="New York")
    neighbourhood: str = Field(example="Bronx")
    address: str = Field(example="123 Main St")
    price: int = Field(example=270000)
    thumbnail: str = Field(example="http://example.com/photo.jpg")
    type: str = Field(example="condo")
    area: int = Field(example=100)
    bed_number: Optional[int] = Field(None, example=3) #Optional field
    bath_number: Optional[int] = Field(None, example=2) #Optional field
    description: Optional[str] = Field(None, example="Beautiful home") #Optional field
    photos: Optional[List[str]] = Field(None, example=["http://example.com/photo1.jpg"]) #Optional field
    disponibility: Optional[Disponibility] = None   #Optional field
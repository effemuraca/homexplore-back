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
    bed_number: Optional[int] = Field(None, example=3) 
    bath_number: Optional[int] = Field(None, example=2) 
    description: Optional[str] = Field(None, example="Beautiful home") 
    photos: Optional[List[str]] = Field(None, example=["http://example.com/photo1.jpg"]) 
    disponibility: Optional[Disponibility] = None   

class UpdatePropertyOnSale(BaseModel):
    property_on_sale_id: Optional[str] = Field(None, example="5f4f4f4f4f4f4f4f4f4f4f4f")
    city: Optional[str] = Field(None, example="New York")
    neighbourhood: Optional[str] = Field(None, example="Bronx")
    address: Optional[str] = Field(None, example="123 Main St")
    price: Optional[int] = Field(None, example=270000)
    thumbnail: Optional[str] = Field(None, example="http://example.com/photo.jpg")
    type: Optional[str] = Field(None, example="condo")
    area: Optional[int] = Field(None, example=100)
    bed_number: Optional[int] = Field(None, example=3) 
    bath_number: Optional[int] = Field(None, example=2) 
    description: Optional[str] = Field(None, example="Beautiful home") 
    photos: Optional[List[str]] = Field(None, example=["http://example.com/photo1.jpg"]) 
    disponibility: Optional[Disponibility] = None   
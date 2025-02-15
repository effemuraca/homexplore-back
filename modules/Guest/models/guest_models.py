from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class FilteredSearchInput(BaseModel):
    city: Optional[str] = Field(None, example="New York")
    address: Optional[str] = Field(None, example="123 Main St", min_length=5)
    neighbourhood: Optional[str] = Field(None, example="Brooklyn")
    max_price: Optional[int] = Field(None, example=500000)
    type: Optional[str] = Field(None, example="House")
    min_area: Optional[int] = Field(None, example=2000)
    min_bed_number: Optional[int] = Field(None, example=3)
    min_bath_number: Optional[int] = Field(None, example=2)
    
    @field_validator('max_price')
    def validate_max_price(cls, value):
        if value and value < 0:
            raise ValueError('Price must be positive.')
        return value
    
    @field_validator('min_area')
    def validate_min_area(cls, value):
        if value and value < 0:
            raise ValueError('Area must be positive.')
        return value
    
    @field_validator('min_bed_number')
    def validate_min_bed_number(cls, value):
        if value and value < 0:
            raise ValueError('Bed number must be positive.')
        return value
    
    @field_validator('min_bath_number')
    def validate_min_bath_number(cls, value):
        if value and value < 0:
            raise ValueError('Bath number must be positive.')
        return value
    

class SummaryPropertyOnSale(BaseModel):
    property_on_sale_id: Optional[str] = None
    city: Optional[str] = None
    neighbourhood: Optional[str] = None
    address: Optional[str] = None
    price: Optional[int] = None
    type: Optional[str] = None
    area: Optional[int] = None
    thumbnail: Optional[str] = None
    registration_date: Optional[datetime] = None
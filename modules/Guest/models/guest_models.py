from pydantic import BaseModel, Field, field_validator
from typing import Optional


class FilteredSearchInput(BaseModel):
    city: Optional[str] = Field(None, example="New York")
    address : Optional[str] = Field(None, example="123 Main St")
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
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
import re

class SuccessModel(BaseModel):
    detail: str

class ErrorModel(BaseModel):
    detail: str

class BookNow(BaseModel):
    buyer_id: str = Field(example="615c44fdf641be001f0c1111")
    property_on_sale_id: str = Field(example="615c44fdf641be001f0c1111")
    day : str = Field(example="Monday")
    time: str = Field(example="10:00 AM")
    thumbnail: str = Field(example="https://www.example.com/image")
    address: str = Field(example="1234 Example St.")
    max_reservations : int = Field(example=10)

    @field_validator('day')
    def validate_day(cls, v):
        if v not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            raise ValueError('Invalid day')
        return v
    
    @field_validator('time')
    def validate_time(cls, v):
        if not re.match(r"^(0?[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$", v):
            raise ValueError('Invalid time')
        return v
    
    @field_validator('thumbnail')
    def validate_thumbnail(cls, v):
        if not v.startswith('https://') or not v.endswith('.jpg'):
            raise ValueError('Invalid thumbnail')
        return v
    
    @field_validator('address')
    def validate_address(cls, v):
        if not re.match(r"^\d{1,5} [A-Z][a-z]+ [A-Z][a-z]+", v):
            raise ValueError('Invalid address')
        return v
    
    @field_validator('max_reservations')
    def validate_max_reservations(cls, v):
        if v < 1 or v > 1000:
            raise ValueError('Invalid max_reservations')
        return v

    
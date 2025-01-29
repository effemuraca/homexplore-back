from pydantic import BaseModel, Field, validator
from typing import List, Optional
import re

class CreateDisponibility(BaseModel):
    day: str = Field(example="Monday")
    time: str = Field(example="10:00-11:00 AM")
    max_attendees: int = Field(example=5)

    @validator("day")
    def validate_day(cls, value):
        valid_days = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}
        if value not in valid_days:
            raise ValueError("Invalid day. Must be one of: " + ", ".join(valid_days))
        return value

    @validator("time")
    def validate_time(cls, value):
        time_pattern = re.compile(r"^(0[1-9]|1[0-2]):[0-5][0-9]-(0[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$")
        if not time_pattern.match(value):
            raise ValueError("Invalid time format. Expected format: HH:MM-HH:MM AM/PM")
        return value

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
    disponibility: Optional[CreateDisponibility] = None   

class UpdateDisponibility(BaseModel):
    day: Optional[str] = Field(None, example="Monday")
    time: Optional[str] = Field(None, example="10:00-11:00 AM")
    max_attendees: Optional[int] = Field(None, example=5)

    @validator("day")
    def validate_day(cls, value):
        valid_days = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}
        if value not in valid_days:
            raise ValueError("Invalid day. Must be one of: " + ", ".join(valid_days))
        return value

    @validator("time")
    def validate_time(cls, value):
        time_pattern = re.compile(r"^(0[1-9]|1[0-2]):[0-5][0-9]-(0[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$")
        if not time_pattern.match(value):
            raise ValueError("Invalid time format. Expected format: HH:MM-HH:MM AM/PM")
        return value

class UpdatePropertyOnSale(BaseModel):
    property_on_sale_id: str = Field(None, example="5f4f4f4f4f4f4f4f4f4f4f4f")
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
    disponibility: Optional[UpdateDisponibility] = None   
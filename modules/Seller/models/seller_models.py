from pydantic import BaseModel, Field, validator, field_validator, EmailStr
from bson import ObjectId 
from typing import Optional, List
import re
from datetime import datetime
import math

# Seller
class UpdateSeller(BaseModel):
    agency_name: Optional[str] = Field(None, example="Agency Name")
    email: Optional[EmailStr] = Field(None, example="email@example.com")
    password: Optional[str] = Field(None, example="password123")


# PropertyOnSale

#CONSISTENT
class CreateDisponibility(BaseModel):
    day: str = Field(..., example="Monday")
    time: str = Field(..., example="10:00 AM - 11:00 AM")
    max_attendees: int = Field(..., example=5)

    @field_validator("day")
    def validate_day(cls, value):
        valid_days = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}
        if value not in valid_days:
            raise ValueError("Invalid day. Must be one of: " + ", ".join(valid_days))
        return value

    @field_validator('time')
    def validate_time(cls, v):
        pattern = r"^(0|0?[1-9]|1[0-2]|13):[0-5][0-9] (AM|PM) - (0|0?[1-9]|1[0-2]|13):[0-5][0-9] (AM|PM)$"
        if not re.match(pattern, v):
            raise ValueError('Invalid time')
        return v
    
    @field_validator('max_attendees')
    def validate_max_attendees(cls, v):
        if v < 1 or v > 1000:
            raise ValueError('Invalid max_attendees')
        return v
    
class CreatePropertyOnSale(BaseModel):
    city: str = Field(..., example="New York")
    neighbourhood: str = Field(..., example="Bronx")
    address: str = Field(..., example="123 Main St")
    price: int = Field(..., example=270000)
    thumbnail: str = Field(..., example="http://example.com/photo.jpg")
    type: str = Field(..., example="condo")
    area: int = Field(..., example=100)
    bed_number: Optional[int] = Field(None, example=3) 
    bath_number: Optional[int] = Field(None, example=2) 
    description: Optional[str] = Field(None, example="Beautiful home") 
    photos: Optional[List[str]] = Field(None, example=["http://example.com/photo1.jpg"]) 
    disponibility: Optional[CreateDisponibility] = Field(None, example={"day": "Monday", "time": "10:00 AM - 11:00 AM", "max_attendees": 5})   
    
    @field_validator("price")
    def validate_price(cls, value):
        if value < 0:
            raise ValueError("Price must be positive")
        return value
    
    @field_validator("thumbnail")
    def validate_thumbnail(cls, value):
        if not re.match(r'^https?://.*\.(?:png|jpg|jpeg|gif)$', value):
            raise ValueError("Invalid URL format")
        return value
    
    @field_validator('area', mode='before')
    def parse_nan_to_zero(cls, value):
        if isinstance(value, float) and math.isnan(value):
            return 0
        return value
    
    @field_validator('area')
    def validate_area(cls, value):
        if value < 0:
            raise ValueError('Area must be positive.')
        return value
    
    @field_validator("bed_number")
    def validate_bed_number(cls, value):
        if value < 0:
            raise ValueError("Bed number must be positive")
        return value
    
    @field_validator("bath_number")
    def validate_bath_number(cls, value):
        if value < 0:
            raise ValueError("Bath number must be positive")
        return value
    
    @field_validator("photos")
    def validate_photos(cls, value):
        for photo in value:
            if not re.match(r'^https?://.*\.(?:png|jpg|jpeg|gif)$', photo):
                raise ValueError("Invalid URL format")
        return value
        

#CONSISTENT
class UpdateDisponibility(BaseModel):
    day: Optional[str] = Field(None, example="Monday")
    time: Optional[str] = Field(None, example="10:00 AM - 11:00 AM")
    max_attendees: Optional[int] = Field(None, example=5)

    @field_validator("day")
    def validate_day(cls, value):
        valid_days = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}
        if value not in valid_days:
            raise ValueError("Invalid day. Must be one of: " + ", ".join(valid_days))
        return value

    @field_validator('time')
    def validate_time(cls, v):
        pattern = r"^(0|0?[1-9]|1[0-2]|13):[0-5][0-9] (AM|PM) - (0|0?[1-9]|1[0-2]|13):[0-5][0-9] (AM|PM)$"
        if not re.match(pattern, v):
            raise ValueError('Invalid time')
        return v
    
    @field_validator('max_attendees')
    def validate_max_attendees(cls, v):
        if v < 1 or v > 1000:
            raise ValueError('Invalid max_attendees')
        return v
    
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
    disponibility: Optional[UpdateDisponibility] = Field(None, example={"day": "Monday", "time": "10:00 AM - 11:00 AM", "max_attendees": 5})   

    @field_validator("property_on_sale_id")
    def validate_property_on_sale_id(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid property_on_sale_id")
        return value
    
    @field_validator("price")
    def validate_price(cls, value):
        if value < 0:
            raise ValueError("Price must be positive")
        return value
    
    @field_validator("thumbnail")
    def validate_thumbnail(cls, value):
        if not re.match(r'^https?://.*\.(?:png|jpg|jpeg|gif)$', value):
            raise ValueError("Invalid URL format")
        return value
    
    @field_validator('area', mode='before')
    def parse_nan_to_zero(cls, value):
        if isinstance(value, float) and math.isnan(value):
            return 0
        return value
    
    @field_validator('area')
    def validate_area(cls, value):
        if value < 0:
            raise ValueError('Area must be positive.')
        return value
    
    @field_validator("bed_number")
    def validate_bed_number(cls, value):
        if value < 0:
            raise ValueError("Bed number must be positive")
        return value
    
    @field_validator("bath_number")
    def validate_bath_number(cls, value):
        if value < 0:
            raise ValueError("Bath number must be positive")
        return value
    
    @field_validator("photos")
    def validate_photos(cls, value):
        for photo in value:
            if not re.match(r'^https?://.*\.(?:png|jpg|jpeg|gif)$', photo):
                raise ValueError("Invalid URL format")
        return value



# Analytics

class Analytics2Input(BaseModel):
    city: str = Field(..., example="New York")
    start_date: str = Field(..., example="2021-01-01")
    end_date: str = Field(..., example="2021-12-31")

    @field_validator("start_date")
    def validate_start_date(cls, value):
        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if not date_pattern.match(value):
            raise ValueError("Invalid date format. Expected format: YYYY-MM-DD")
        return value
    
    @field_validator("end_date")
    def validate_end_date(cls, value):
        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if not date_pattern.match(value):
            raise ValueError("Invalid date format. Expected format: YYYY-MM-DD")
        return value
    
class Analytics3Input(BaseModel):
    city: str = Field(..., example="New York")
    start_date: str = Field(..., example="2021-01-01")

    @field_validator("start_date")
    def validate_start_date(cls, value):
        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if not date_pattern.match(value):
            raise ValueError("Invalid date format. Expected format: YYYY-MM-DD")
        return value
    
   
    
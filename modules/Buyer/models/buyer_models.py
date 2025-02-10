from pydantic import BaseModel, Field, field_validator
from typing import Optional
from pydantic.networks import EmailStr
from bson import ObjectId
import re

class UpdateBuyer(BaseModel):
    email: Optional[EmailStr] = Field(None, example="john.doe@example.com")
    password: Optional[str] = Field(None, example="SecureP@ssw0rd")
    name: Optional[str] = Field(None, example="John")
    surname: Optional[str] = Field(None, example="Doe")
    phone_number: Optional[str] = Field(None, example="+1 1234567890")
    
    @field_validator('phone_number')
    def validate_phone_number(cls, value):
        if value:
            phone_pattern = re.compile(r'^\+\d{1,3}\s?\d{7,14}$')
            if not phone_pattern.match(value):
                raise ValueError('Invalid phone number format.')
        return value

    

class CreateReservationBuyer(BaseModel):
    property_on_sale_id: str = Field(example="615c44fdf641be001f0c1111")
    day : str = Field(example="Monday")
    time: str = Field(example="10:00-11:00 AM")
    thumbnail: str = Field(example="https://www.example.com/image.png")
    address: str = Field(example="1234 Example St.")
    max_attendees : int = Field(example=10)

    @field_validator('property_on_sale_id')
    def validate_property_on_sale_id(cls, v):
        if not re.match(r"^[a-f\d]{24}$", v):
            raise ValueError('Invalid property_on_sale_id')
        return v
    
    @field_validator('day')
    def validate_day(cls, v):
        if v not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            raise ValueError('Invalid day')
        return v
    
    @field_validator('time')
    def validate_time(cls, v):
        if not re.match(r"^(0?[1-9]|1[0-2]):[0-5][0-9]-(0?[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$", v):
            raise ValueError('Invalid time')
        return v
    
    @field_validator('thumbnail')
    def validate_thumbnail(cls, v):
        if not re.match(r'^https?://.*\.(?:png|jpg|jpeg|gif)$', v):
            raise ValueError('Invalid URL format.')
        return v
    
    
    @field_validator('max_attendees')
    def validate_max_attendees(cls, v):
        if v < 1 or v > 1000:
            raise ValueError('Invalid max_attendees')
        return v
    

class UpdateReservationBuyer(BaseModel):
    property_on_sale_id: str = Field(example="615c44fdf641be001f0c1111")
    buyer_id: str = Field(example="615c44fdf641be001f0c1111")
    date: str = Field(example="2021-09-01")
    time: str = Field(example="10:00-11:00 AM")
    thumbnail: str = Field(example="https://www.example.com/image.png")
    address: str = Field(example="1234 Example St.")
    
    @field_validator('property_on_sale_id')
    def check_property_on_sale_id(cls, v: str) -> str:
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId string')
        return v

    @field_validator('buyer_id')
    def check_buyer_id(cls, v: str) -> str:
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId string')
        return v
    
    @field_validator('date')
    def check_date_format(cls, v: str) -> str:
        if not re.match(r'\d{4}-\d{2}-\d{2}', v):
            raise ValueError('Invalid date format')
        return v
    
    @field_validator("time")
    def validate_time(cls, value):
        time_pattern = re.compile(r"^(0[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$")
        if not time_pattern.match(value):
            raise ValueError("Invalid time format. Expected format: HH:MM AM/PM")
        return value
    
    @field_validator('thumbnail')
    def check_url(cls, v: str) -> str:
        if not re.match(r'^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$', v):
            raise ValueError('Invalid URL format')
        return v

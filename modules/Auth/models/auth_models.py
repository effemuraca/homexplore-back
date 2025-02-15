from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re


class Login(BaseModel):
    email: EmailStr = Field(..., example="email@example.com")
    password: str = Field(...,max_length=32, example="ThisIsAPassword123!")

class CreateSeller(BaseModel):
    agency_name: str = Field(..., example="Agency Name")
    email: EmailStr = Field(..., example="john.doe@seller.com")
    password: str = Field(..., example="password123")

class CreateBuyer(BaseModel):
    email: EmailStr = Field(..., example="john.doe@buyer.com")
    password: str = Field(..., example="SecureP@ssw0rd")
    name: str = Field(..., example="John")
    surname: str = Field(..., example="Doe")
    phone_number: str = Field(..., example="+39 1234567890")
    
    @field_validator("phone_number")
    def validate_phone_number(cls, value):
        phone_pattern = re.compile(r"^\+\d{2} \d{10}$")
        if not phone_pattern.match(value):
            raise ValueError("Invalid phone number format. Expected format: +xx xxxxxxxxxx")
        return value
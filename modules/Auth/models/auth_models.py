from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import re


class Login(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=32, example="ThisIsAPassword123!")

class CreateSeller(BaseModel):
    agency_name: str = Field(example="Agency Name")
    email: EmailStr = Field(example="email@example.com")
    password: str = Field(example="password123")

class CreateBuyer(BaseModel):
    email: EmailStr = Field(None, example="john.doe@example.com")
    password: str = Field(None, example="SecureP@ssw0rd")
    name: str = Field(None, example="John")
    surname: str = Field(None, example="Doe")
    phone_number: Optional[str] = Field(None, example="+39 1234567890")
    
    @validator("phone_number")
    def validate_phone_number(cls, value):
        phone_pattern = re.compile(r"^\+\d{2} \d{10}$")
        if not phone_pattern.match(value):
            raise ValueError("Invalid phone number format. Expected format: +xx xxxxxxxxxx")
        return value
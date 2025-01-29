from pydantic import BaseModel, Field, validator
from typing import Optional
import re


class CreateSeller(BaseModel):
    agency_name: str = Field(example="Agency Name")
    email: str = Field(example="email@example.com")
    password: str = Field(example="password123")
    phone_number: str = Field(example="+38 1234567890")
    
    @validator("email")
    def validate_email(cls, value):
        email_pattern = re.compile(
            r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        )
        if not email_pattern.match(value):
            raise ValueError("Invalid email format. Expected format: email@example.com")
        return value

    @validator("phone_number")
    def validate_phone_number(cls, value):
        phone_pattern = re.compile(r"^\+\d{2} \d{10}$")
        if not phone_pattern.match(value):
            raise ValueError("Invalid phone number format. Expected format: +xx xxxxxxxxxx")
        return value

class UpdateSeller(BaseModel):
    seller_id: str = Field(..., example="5f4f4f4f4f4f4f4f4f4f4f4f")
    agency_name: Optional[str] = Field(None, example="Agency Name")
    email: Optional[str] = Field(None, example="email@example.com")
    password: Optional[str] = Field(None, example="password123")
    phone_number: Optional[str] = Field(None, example="+38 1234567890")
    
    @validator("email")
    def validate_email(cls, value):
        email_pattern = re.compile(
            r"^(?!\.)(""([^""\r\\]|\\[""\r\\])*""|"
            r"([-!#\$%&'\*\+/=\?\^`\{\}\|~\w]+(?:\.[-!#\$%&'\*\+/=\?\^`\{\}\|~\w]+)*)"
            r")@((?:[A-Z0-9-]+\.)+[A-Z]{2,})$", re.IGNORECASE)
        if not email_pattern.match(value):
            raise ValueError("Invalid email format. Expected format: email@example.com")
        return value

    @validator("phone_number")
    def validate_phone_number(cls, value):
        phone_pattern = re.compile(r"^\+\d{2} \d{10}$")
        if not phone_pattern.match(value):
            raise ValueError("Invalid phone number format. Expected format: +xx xxxxxxxxxx")
        return value

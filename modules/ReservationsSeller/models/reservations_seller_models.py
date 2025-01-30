from pydantic import BaseModel, Field
from typing import Optional


class CreateReservationSeller(BaseModel):
    property_id: str = Field(example="615c44fdf641be001f0c1111")
    buyer_id: str = Field(None, example="615c44fdf641be001f0c1111")
    full_name: str = Field(None, example="John Doe")
    email: str = Field(None, example="john@example.com")
    phone: str = Field(None, example="1234567890")
    seconds: int = Field(0, example=3600)  

class UpdateReservationSeller(BaseModel):
    property_id: str = Field(example="615c44fdf641be001f0c1111")
    buyer_id: Optional[str] = Field(None, example="615c44fdf641be001f0c1111")
    full_name: Optional[str] = Field(None, example="John Doe")
    email: Optional[str] = Field(None, example="john@example.com")
    phone: Optional[str] = Field(None, example="1234567890")

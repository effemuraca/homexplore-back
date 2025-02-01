from pydantic import BaseModel, Field
from typing import Optional, List
from entities.ReservationsSeller.reservations_seller import ReservationS

class CreateReservationSeller(BaseModel):
    property_on_sale_id: str = Field(..., example="615c44fdf641be001f0c1111")
    buyer_id: Optional[str] = Field(None, example="615c44fdf641be001f0c1111")
    full_name: Optional[str] = Field(None, example="John Doe")
    email: Optional[str] = Field(None, example="john@example.com")
    phone: Optional[str] = Field(None, example="1234567890")
    day: str = Field(..., example="Monday")
    time: str = Field(..., example="12:00 PM")
    area: int = Field(..., example=500)

class UpdateReservationSeller(BaseModel):
    property_on_sale_id: str = Field(..., example="615c44fdf641be001f0c1111")
    buyer_id: Optional[str] = Field(None, example="615c44fdf641be001f0c1111")
    full_name: Optional[str] = Field(None, example="John Doe")
    email: Optional[str] = Field(None, example="john@example.com")
    phone: Optional[str] = Field(None, example="1234567890")

class UpdateEntireReservationSeller(BaseModel):
    property_on_sale_id: str = Field(..., example="615c44fdf641be001f0c1111")
    area: Optional[int] = Field(None, example=500)
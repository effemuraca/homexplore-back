from pydantic import BaseModel, Field
from typing import Optional, List

class ReservationS(BaseModel):
    buyer_id: Optional[str] = Field(None, example=1)
    full_name: Optional[str] = Field(None, example="John Doe")
    email: Optional[str] = Field(None, example="john@example.com")
    phone: Optional[str] = Field(None, example="1234567890")

class ReservationsSeller(BaseModel):
    property_id: Optional[str] = Field(None, example=1)
    reservations: Optional[List[ReservationS]] = None
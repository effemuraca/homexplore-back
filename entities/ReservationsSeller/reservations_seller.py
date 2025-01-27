from pydantic import BaseModel
from typing import Optional, List

class ReservationS(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class ReservationsSeller(BaseModel):
    property_id: Optional[int] = None
    reservations: Optional[List[ReservationS]] = None
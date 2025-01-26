from pydantic import BaseModel
from typing import Optional, List
import json
class ReservationS(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    def __init__(
        self, 
        full_name: str = None, 
        email: str = None, 
        phone: str = None
    ):
        super().__init__()
        self.full_name = full_name
        self.email = email
        self.phone = phone

class ReservationsSeller(BaseModel):
    property_id: Optional[int] = None
    reservations: Optional[List[ReservationS]] = None

    def __init__(
        self, 
        property_id: int = None, 
        reservations: List[ReservationS] = None
    ):
        super().__init__()
        self.property_id = property_id
        self.reservations = reservations
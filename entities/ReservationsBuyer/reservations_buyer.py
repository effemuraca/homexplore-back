from pydantic import BaseModel
from typing import Optional, List

class ReservationB(BaseModel):
    property_id: Optional[int] = None
    date: Optional[str] = None
    time: Optional[str] = None
    thumbnail: Optional[str] = None
    address: Optional[str] = None

class ReservationsBuyer(BaseModel):
    buyer_id: Optional[int] = None
    reservations: Optional[List[ReservationB]] = None
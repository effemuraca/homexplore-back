from pydantic import BaseModel
from typing import Optional, List
class ReservationB(BaseModel):
    property_id: Optional[int] = None
    date: Optional[str] = None
    time: Optional[str] = None
    thumbnail: Optional[str] = None
    address: Optional[str] = None

    def __init__(
        self,
        property_id: int,
        date: str,
        time: str,
        thumbnail: str,
        address: str
    ):
        super().__init__()
        self.property_id = property_id
        self.date = date
        self.time = time
        self.thumbnail = thumbnail
        self.address = address

class ReservationsBuyer(BaseModel):
    buyer_id: Optional[int] = None
    reservations: Optional[List[ReservationB]] = None

    def __init__(
        self, 
        buyer_id: int = None, 
        reservations: list[ReservationB] = None
    ):
        super().__init__()
        self.buyer_id = buyer_id
        self.reservations = reservations


   
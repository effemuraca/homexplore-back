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

    def count_reservations_by_open_house(self) -> int:
        return len(self.reservations) if self.reservations else 0

    def get_attendees_json(self) -> str:
        return json.dumps([r.model_dump() for r in self.reservations]) if self.reservations else "[]"
    
    # this entity is related to:
    # - A new reservation is made by a buyer -> I need to store his info in the reservations list
    # - A reservation is canceled by a buyer -> I need to remove his info from the reservations list
    # - View reservations clicked by a seller (mongoID known) -> I need to return the reservations list
    # - A property is sold -> I need to remove all reservations related to this property
    # - A property is removed -> I need to remove all reservations related to this property
    # - A buyer changes his contact info -> I need to update his info in the reservations list
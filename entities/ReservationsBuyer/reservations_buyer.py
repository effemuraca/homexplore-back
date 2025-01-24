from pydantic import BaseModel
from typing import Optional, List
class ReservationB(BaseModel):
    property_id: Optional[int] = None
    open_house_id: Optional[int] = None
    date: Optional[str] = None
    time: Optional[str] = None
    thumbnail: Optional[str] = None
    property_type: Optional[str] = None
    price: Optional[int] = None
    address: Optional[str] = None

    def __init__(
        self,
        property_id: int,
        open_house_id: int,
        date: str,
        time: str,
        thumbnail: str,
        property_type: str,
        price: int,
        address: str
    ):
        super().__init__()
        self.property_id = property_id
        self.open_house_id = open_house_id
        self.date = date
        self.time = time
        self.thumbnail = thumbnail
        self.property_type = property_type
        self.price = price
        self.address = address

class ReservationsBuyer(BaseModel):
    user_id: Optional[int] = None
    reservations: Optional[List[ReservationB]] = None

    def __init__(self, user_id: int = None, reservations: list[ReservationB] = None):
        super().__init__()
        self.user_id = user_id
        self.reservations = reservations


    # this entity is related to:
    # - A new reservation is made by a buyer -> I need to store his info in the reservations list
    # - A reservation is canceled by a buyer -> I need to remove his info from the reservations list
    # - View reservations clicked by a seller (mongoID known) -> I need to return the reservations list
    # - A property is sold -> I need to remove all reservations related to this property
    # - A property is removed -> I need to remove all reservations related to this property
    # - A buyer changes his contact info -> I need to update his info in the reservations list
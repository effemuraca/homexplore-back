import json
class ReservationS:
    user_id:int = None
    full_name:str = None
    email:str = None
    phone:str = None

    def __init__(self, user_id: int, full_name: str, email: str, phone: str):
        self.user_id = user_id
        self.full_name = full_name
        self.email = email
        self.phone = phone

class ReservationsSeller:
    property_id:int = None
    reservations: list[ReservationS] = None
    
    def __init__(self, property_id: int, reservations: list[ReservationS]):
        self.property_id = property_id
        self.reservations = reservations

    def count_reservations_by_open_house(self) -> int:
        return len(self.reservations)
    
    def check_limit_reservations(self) -> bool:
        # to define if we want a static limit (such as this case) or a dynamic limit (based on the open house event)
        return len(self.reservations) >= 10
    
    def get_attendees_json(self) -> str:
        return json.dumps(self.reservations)
    
    # this entity is related to:
    # - A new reservation is made by a buyer -> I need to store his info in the reservations list
    # - A reservation is canceled by a buyer -> I need to remove his info from the reservations list
    # - View reservations clicked by a seller (mongoID known) -> I need to return the reservations list
    # - A property is sold -> I need to remove all reservations related to this property
    # - A property is removed -> I need to remove all reservations related to this property
    # - A buyer changes his contact info -> I need to update his info in the reservations list
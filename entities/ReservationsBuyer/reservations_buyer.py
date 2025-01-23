class ReservationB:
    property_id: int = None
    open_house_id: int = None
    date: str = None
    time: str = None
    thumbnail: str = None
    property_type: str = None
    price: int = None
    address: str = None

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
        self.property_id = property_id
        self.open_house_id = open_house_id
        self.date = date
        self.time = time
        self.thumbnail = thumbnail
        self.property_type = property_type
        self.price = price
        self.address = address

class ReservationsBuyer:
    user_id: int = None
    reservations: list[ReservationB] = None

    def __init__(self, user_id: int, reservations: list[ReservationB]):
        self.user_id = user_id
        self.reservations = reservations


    # this entity is related to:
    # - A new reservation is made by a buyer -> I need to store his info in the reservations list
    # - A reservation is canceled by a buyer -> I need to remove his info from the reservations list
    # - View reservations clicked by a seller (mongoID known) -> I need to return the reservations list
    # - A property is sold -> I need to remove all reservations related to this property
    # - A property is removed -> I need to remove all reservations related to this property
    # - A buyer changes his contact info -> I need to update his info in the reservations list
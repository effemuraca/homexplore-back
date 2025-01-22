class ReservationB:
    property_id:int = None
    open_house_id:int = None
    date:str = None
    time:str = None

    def __init__(self, property, open_house_id, date, time):
        self.property_id = property
        self.open_house_id = open_house_id
        self.date = date
        self.time = time

class ReservationsBuyer:
    user_id:int = None
    reservation:ReservationB = None
    
    def __init__(self, user_id:int, reservation:ReservationB):
        self.user_id = user_id
        self.reservation = reservation

class ReservationS:
    user_id:int = None
    full_name:str = None
    email:str = None
    phone:str = None

    def __init__(self, user_id, full_name, email, phone):
        self.user_id = user_id
        self.full_name = full_name
        self.email = email
        self.phone = phone

class ReservationsSeller:
    open_house_id:int = None
    reservation:ReservationS = None
    
    def __init__(self, open_house_id:int, reservation:ReservationS):
        self.open_house_id = open_house_id
        self.reservation = reservation

from entities.ReservationsBuyer.reservations_buyer import ReservationsBuyer
from setup.redis_setup.redis_setup import get_redis_client

class ReservationsBuyerDB:
    reservations_buyer:ReservationsBuyer = None
    
    def __init__(self, reservations_buyer:ReservationsBuyer):
        self.reservations_buyer = reservations_buyer
        
    def get_reservations_buyer_by_attribute(self, attribute:str):
        redis_client = get_redis_client()

    
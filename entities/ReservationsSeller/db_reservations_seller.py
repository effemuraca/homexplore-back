from entities.ReservationsSeller.reservations_seller import ReservationsSeller
from setup.redis_setup.redis_setup import get_redis_client

class ReservationsBuyerDB:
    reservations_seller:ReservationsSeller = None
    
    def __init__(self, reservations_seller:ReservationsSeller):
        self.reservations_seller = reservations_seller
        
    def get_reservations_seller_by_attribute(self, attribute:str):
        redis_client = get_redis_client()

    
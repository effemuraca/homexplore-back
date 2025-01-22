import json
from entities.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS
from setup.redis_setup.redis_setup import get_redis_client

class ReservationsSellerDB:
    reservations_seller:ReservationsSeller = None
    
    def __init__(self, reservations_seller:ReservationsSeller):
        self.reservations_seller = reservations_seller
        
    def get_reservations_seller_by_open_house(self, open_house_id:int) -> ReservationsSeller:
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"open_house:{open_house_id}")
        if not raw_data:
            return None
        data = json.loads(raw_data)
        reservation = ReservationS(
            user_id=data["user_id"],
            full_name=data["full_name"],
            email=data["email"],
            phone=data["phone"]
        )
        return ReservationsSeller(open_house_id=open_house_id, reservation=reservation)

    def delete_reservations_seller_by_open_house(self, open_house_id: int) -> bool:
        redis_client = get_redis_client()
        result = redis_client.delete(f"open_house:{open_house_id}")
        return bool(result)
    
    # todo: implement the following methods
    # create reservation 
    # update reservation (contact info updated in mongo)
    # given a property_id, get all the contact info of the buyers who reserved an open house event for this property
    # count reservations by open house event
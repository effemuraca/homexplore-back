import json
from entities.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB
from setup.redis_setup.redis_setup import get_redis_client

class ReservationsBuyerDB:
    reservations_buyer:ReservationsBuyer = None
    
    def __init__(self, reservations_buyer:ReservationsBuyer):
        self.reservations_buyer = reservations_buyer
        
    def get_reservations_buyer_by_user(self, user_id:int) -> ReservationsBuyer:
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"user:{user_id}")
        if not raw_data:
            return None
        data = json.loads(raw_data)
        reservation = ReservationB(
            property_id=data["property_id"],
            open_house_id=data["open_house_id"],
            date=data["date"],
            time=data["time"]
        )
        return ReservationsBuyer(user_id=user_id, reservation=reservation)
    

    def delete_reservations_buyer_by_user(self, user_id: int) -> bool:
        redis_client = get_redis_client()
        result = redis_client.delete(f"user:{user_id}")
        return bool(result)

    # todo: implement the following methods
    # create reservation 
    # update reservation (open house event updated in mongo)
    # count reservations by property

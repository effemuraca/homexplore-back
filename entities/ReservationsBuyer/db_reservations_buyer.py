import json
from entities.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB
from setup.redis_setup.redis_setup import get_redis_client

class ReservationsBuyerDB:
    reservations_buyer:ReservationsBuyer = None
    
    def __init__(self, reservations_buyer:ReservationsBuyer):
        self.reservations_buyer = reservations_buyer
        
    def get_reservations_buyer_by_user(self, user_id:int) -> ReservationsBuyer:
        if not user_id:
            return None
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
        if not user_id:
            return False
        redis_client = get_redis_client()
        result = redis_client.delete(f"user:{user_id}")
        return bool(result)
    
    def create_reservations_buyer(self, user_id:int, reservation:ReservationB) -> bool:
        if not user_id:
            return False
        if not reservation:
            return False
        redis_client = get_redis_client()
        data = {
            "property_id": reservation.property_id,
            "open_house_id": reservation.open_house_id,
            "date": reservation.date,
            "time": reservation.time
        }
        result = redis_client.set(f"user:{user_id}", json.dumps(data))
        return bool(result)
    
    def update_reservations_buyer(self, user_id:int = None, reservation:ReservationB = None) -> bool:
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"user:{user_id}")
        if not raw_data:
            return False
        data = json.loads(raw_data)
        if reservation.property_id:
            data["property_id"] = reservation.property_id
        if reservation.open_house_id:
            data["open_house_id"] = reservation.open_house_id
        if reservation.date:
            data["date"] = reservation.date
        if reservation.time:
            data["time"] = reservation.time
        result = redis_client.set(f"user:{user_id}", json.dumps(data))
        return bool(result)
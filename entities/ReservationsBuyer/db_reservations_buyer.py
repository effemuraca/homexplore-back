import json
from entities.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB
from setup.redis_setup.redis_setup import get_redis_client

class ReservationsBuyerDB:
    reservations_buyer: ReservationsBuyer = None
    
    def __init__(self, reservations_buyer: ReservationsBuyer):
        self.reservations_buyer = reservations_buyer

    def get_reservations_by_user(self, user_id: int) -> ReservationsBuyer:
        if not user_id:
            return None
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"buyer_id:{user_id}:reservations")
        if not raw_data:
            return None
        data = json.loads(raw_data)
        reservation_list = []
        for item in data:
            reservation_list.append(ReservationB(**item))
        self.reservations_buyer = ReservationsBuyer(buyer_id=user_id, reservations=reservation_list)
        return self.reservations_buyer

    def delete_reservations_by_user(self, user_id: int) -> bool:
        if not user_id:
            return False
        redis_client = get_redis_client()
        result = redis_client.delete(f"buyer_id:{user_id}:reservations")
        return bool(result)

    def create_reservation(self, user_id: int, reservation: ReservationB) -> bool:
        if not user_id or not reservation:
            return False
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"buyer_id:{user_id}:reservations")
        if not raw_data:
            data = []
        else:
            data = json.loads(raw_data)
        data.append({
            "property_id": reservation.property_id,
            "date": reservation.date,
            "time": reservation.time,
            "thumbnail": reservation.thumbnail,
            "address": reservation.address
        })
        result = redis_client.set(f"buyer_id:{user_id}:reservations", json.dumps(data))
        return bool(result)

    def update_reservation(self, user_id: int, reservation: ReservationB) -> bool:
        if not user_id or not reservation:
            return False
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"buyer_id:{user_id}:reservations")
        if not raw_data:
            return False
        data = json.loads(raw_data)
        found = False
        for item in data:
            if item.get("property_id") == reservation.property_id:
                if reservation.date is not None:
                    item["date"] = reservation.date
                if reservation.time is not None:
                    item["time"] = reservation.time
                if reservation.thumbnail is not None:
                    item["thumbnail"] = reservation.thumbnail
                if reservation.address is not None:
                    item["address"] = reservation.address
                found = True
                break
        if not found:
            return False
        result = redis_client.set(f"buyer_id:{user_id}:reservations", json.dumps(data))
        return bool(result)
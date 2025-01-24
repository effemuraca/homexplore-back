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
        raw_data = redis_client.get(f"user:{user_id}:reservations")
        if not raw_data:
            return None
        data = json.loads(raw_data)
        reservation_list = []
        for item in data:
            reservation_list.append(
                ReservationB(
                    property_id=item["property_id"],
                    open_house_id=item["open_house_id"],
                    date=item["date"],
                    time=item["time"],
                    thumbnail=item["thumbnail"],
                    property_type=item["property_type"],
                    price=item["price"],
                    address=item["address"]
                )
            )
        self.reservations_buyer = ReservationsBuyer(user_id=user_id, reservations=reservation_list)
        return self.reservations_buyer

    def delete_reservations_by_user(self, user_id: int) -> bool:
        if not user_id:
            return False
        redis_client = get_redis_client()
        result = redis_client.delete(f"user:{user_id}:reservations")
        return bool(result)

    def create_reservation(self, user_id: int, reservation: ReservationB) -> bool:
        if not user_id or not reservation:
            return False
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"user:{user_id}:reservations")
        if not raw_data:
            data = []
        else:
            data = json.loads(raw_data)
        data.append({
            "property_id": reservation.property_id,
            "open_house_id": reservation.open_house_id,
            "date": reservation.date,
            "time": reservation.time,
            "thumbnail": reservation.thumbnail,
            "property_type": reservation.property_type,
            "price": reservation.price,
            "address": reservation.address
        })
        result = redis_client.set(f"user:{user_id}:reservations", json.dumps(data))
        return bool(result)

    def update_reservation(self, user_id: int = None, reservation: ReservationB = None) -> bool:
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"user:{user_id}:reservations")
        if not raw_data:
            return False
        data = json.loads(raw_data)
        for item in data:
            if item["property_id"] == reservation.property_id and item["open_house_id"] == reservation.open_house_id:
                if reservation.date:
                    item["date"] = reservation.date
                if reservation.time:
                    item["time"] = reservation.time
                if reservation.thumbnail:
                    item["thumbnail"] = reservation.thumbnail
                if reservation.property_type:
                    item["property_type"] = reservation.property_type
                if reservation.price:
                    item["price"] = reservation.price
                if reservation.address:
                    item["address"] = reservation.address
                break
        result = redis_client.set(f"user:{user_id}:reservations", json.dumps(data))
        return bool(result)
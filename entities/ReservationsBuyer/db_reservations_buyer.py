import json
from entities.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB
from setup.redis_setup.redis_setup import get_redis_client

class ReservationsBuyerDB:
    reservations_buyer: ReservationsBuyer = None
    
    def __init__(self, reservations_buyer: ReservationsBuyer):
        self.reservations_buyer = reservations_buyer

    def get_reservations_by_buyer_id(self, buyer_id: int) -> ReservationsBuyer:
        if not buyer_id:
            return None
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"buyer_id:{buyer_id}:reservations")
        if not raw_data:
            return None
        data = json.loads(raw_data)
        reservation_list = []
        for item in data:
            reservation_list.append(
                ReservationB(
                    property_id=item["property_id"],
                    date=item["date"],
                    time=item["time"],
                    thumbnail=item["thumbnail"],
                    address=item["address"]
                )
            )
        self.reservations_buyer = ReservationsBuyer(buyer_id=buyer_id, reservations=reservation_list)
        return True

    def delete_reservations_by_buyer_id(self, buyer_id: int) -> bool:
        if not buyer_id:
            return False
        redis_client = get_redis_client()
        result = redis_client.delete(f"buyer_id:{buyer_id}:reservations")
        return bool(result)

    def create_reservation(self, buyer_id: int, reservation: ReservationB) -> bool:
        if not buyer_id or not reservation:
            return False
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"buyer_id:{buyer_id}:reservations")
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
        result = redis_client.set(f"buyer_id:{buyer_id}:reservations", json.dumps(data))
        return bool(result)

    def update_reservation(self, buyer_id: int = None, reservation: ReservationB = None) -> bool:
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"buyer_id:{buyer_id}:reservations")
        if not raw_data:
            return False
        data = json.loads(raw_data)
        for item in data:
            if item["property_id"] == reservation.property_id:
                if reservation.date:
                    item["date"] = reservation.date
                if reservation.time:
                    item["time"] = reservation.time
                if reservation.thumbnail:
                    item["thumbnail"] = reservation.thumbnail
                if reservation.address:
                    item["address"] = reservation.address
                break
        result = redis_client.set(f"buyer_id:{buyer_id}:reservations", json.dumps(data))
        return bool(result)
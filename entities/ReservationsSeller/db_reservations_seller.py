import json
from entities.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS
from setup.redis_setup.redis_setup import get_redis_client

class ReservationsSellerDB:
    reservations_seller:ReservationsSeller = None
    
    def __init__(self, reservations_seller:ReservationsSeller):
        self.reservations_seller = reservations_seller
        
    def get_reservations_seller_by_open_house(self, open_house_id:int) -> ReservationsSeller:
        if not open_house_id:
            return None
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"open_house:{open_house_id}")
        if not raw_data:
            return None
        data = json.loads(raw_data)
        reservations_list = []
        for item in data:
            reservations_list.append(ReservationS(
                user_id=item["user_id"],
                full_name=item["full_name"],
                email=item["email"],
                phone=item["phone"]
            ))
        return ReservationsSeller(open_house_id=open_house_id, reservations=reservations_list)

    def delete_reservations_seller_by_open_house(self, open_house_id: int) -> bool:
        if not open_house_id:
            return False
        redis_client = get_redis_client()
        result = redis_client.delete(f"open_house:{open_house_id}")
        return bool(result)
    
    def create_reservations_seller(self, open_house_id:int, reservation:ReservationS) -> bool:
        if not open_house_id:
            return False
        if not reservation:
            return False
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"open_house:{open_house_id}:reservations")
        if not raw_data:
            data = []
        else:
            data = json.loads(raw_data)
        data.append({
            "user_id": reservation.user_id,
            "full_name": reservation.full_name,
            "email": reservation.email,
            "phone": reservation.phone
        })
        result = redis_client.set(f"open_house:{open_house_id}:reservations", json.dumps(data))
        return bool(result)
    
    def update_reservations_seller(self, open_house_id:int = None, reservation:ReservationS = None) -> bool:
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"open_house:{open_house_id}")
        if not raw_data:
            return False
        data = json.loads(raw_data)
        for item in data:
            if item["user_id"] == reservation.user_id:
                if reservation.full_name:
                    item["full_name"] = reservation.full_name
                if reservation.email:
                    item["email"] = reservation.email
                if reservation.phone:
                    item["phone"] = reservation.phone
                updated = True
                break
        result = redis_client.set(f"open_house:{open_house_id}:reservations", json.dumps(data))
        return bool(result)
import json
from entities.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS
from setup.redis_setup.redis_setup import get_redis_client

class ReservationsSellerDB:
    reservations_seller:ReservationsSeller = None
    
    def __init__(self, reservations_seller:ReservationsSeller):
        self.reservations_seller = reservations_seller
        
    def get_reservations_seller_by_property_id(self, property_id:int) -> ReservationsSeller:
        if not property_id:
            return None
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:reservations")
        if not raw_data:
            return None
        data = json.loads(raw_data)
        reservations_list = []
        for item in data:
            reservations_list.append(
                ReservationS(
                    full_name=item["full_name"],
                    email=item["email"],
                    phone=item["phone"]
                )
            )
        self.reservations_seller = ReservationsSeller(property_id=property_id, reservations=reservations_list)
        return True

    def delete_reservations_seller_by_property_id(self, property_id: int) -> bool:
        if not property_id:
            return False
        redis_client = get_redis_client()
        result = redis_client.delete(f"property_id:{property_id}:reservations")
        return bool(result)
    
    def create_reservations_seller(self, property_id:int, reservation:ReservationS) -> bool:
        if not property_id or not reservation:
            return False
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:reservations")
        if not raw_data:
            data = []
        else:
            data = json.loads(raw_data)
        data.append({
            "full_name": reservation.full_name,
            "email": reservation.email,
            "phone": reservation.phone
        })
        result = redis_client.set(f"property_id:{property_id}:reservations", json.dumps(data))
        return bool(result)
    
    def update_reservations_seller(self, property_id:int = None, reservation:ReservationS = None) -> bool:
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:reservations")
        if not raw_data:
            return False
        data = json.loads(raw_data)
        for item in data:
            if reservation.full_name:
                item["full_name"] = reservation.full_name
            if reservation.email:
                item["email"] = reservation.email
            if reservation.phone:
                item["phone"] = reservation.phone
            break
        result = redis_client.set(f"property_id:{property_id}:reservations", json.dumps(data))
        return bool(result)
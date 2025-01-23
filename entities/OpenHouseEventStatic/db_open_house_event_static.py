import json
from entities.OpenHouseEventStatic.open_house_event_static import OpenHouseEventStatic, StaticInfo
from setup.redis_setup.redis_setup import get_redis_client

class OpenHouseEventStaticDB:
    open_house_event_static:OpenHouseEventStatic = None
    
    def __init__(self, open_house_event_static:OpenHouseEventStatic):
        self.open_house_event_static = open_house_event_static
    
    def get_open_house_event_static_by_property(self, property_id:int) -> OpenHouseEventStatic:
        if not property_id:
            return None
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"static_info:{property_id}")
        if not raw_data:
            return None
        data = json.loads(raw_data)
        static_info = StaticInfo(
            event_id=data["event_id"],
            thumbnail=data["thumbnail"],
            type=data["type"],
            price=data["price"],
            address=data["address"],
            time_schedule=data["time_schedule"]
        )
        return OpenHouseEventStatic(property_id=property_id, static_info=static_info)
   
    def delete_open_house_event_static_by_property(self, property_id: int) -> bool:
        if not property_id:
            return False
        redis_client = get_redis_client()
        result = redis_client.delete(f"static_info:{property_id}")
        return bool(result)

    def create_open_house_event_static(self, property_id:int, static_info:StaticInfo) -> bool:
        if not property_id:
            return False
        if not static_info:
            return False
        redis_client = get_redis_client()
        data = {
            "event_id": static_info.event_id,
            "thumbnail": static_info.thumbnail,
            "type": static_info.type,
            "price": static_info.price,
            "address": static_info.address,
            "time_schedule": static_info.time_schedule

        }
        result = redis_client.set(f"static_info:{property_id}", json.dumps(data))
        return bool(result)
    
    def update_open_house_event_static(self, property_id:int = None, static_info:StaticInfo = None) -> bool:
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"static_info:{property_id}")
        if not raw_data:
            return False
        data = json.loads(raw_data)
        if static_info.event_id:
            data["event_id"] = static_info.event_id
        if static_info.thumbnail:
            data["thumbnail"] = static_info.thumbnail
        if static_info.type:
            data["type"] = static_info.type
        if static_info.price:
            data["price"] = static_info.price
        if static_info.address:
            data["address"] = static_info.address
        if static_info.time_schedule:
            data["time_schedule"] = static_info.time_schedule
        result = redis_client.set(f"static_info:{property_id}", json.dumps(data))
        return bool(result)
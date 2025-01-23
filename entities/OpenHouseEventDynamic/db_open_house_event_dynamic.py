import json
from entities.OpenHouseEventDynamic.open_house_event_dynamic import OpenHouseEventDynamic, DynamicInfo
from setup.redis_setup.redis_setup import get_redis_client

class OpenHouseEventDynamicDB:
    open_house_event_dynamic:OpenHouseEventDynamic = None
    
    def __init__(self, open_house_event_dynamic:OpenHouseEventDynamic):
        self.open_house_event_dynamic = open_house_event_dynamic
    
    def get_open_house_event_dynamic_by_property(self, property_id:int) -> OpenHouseEventDynamic:
        if not property_id:
            return None
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:dynamic_info")
        if not raw_data:
            return None
        data = json.loads(raw_data)
        dynamic_info = DynamicInfo(
            date=data["date"],
            time=data["time"]
        )
        return OpenHouseEventDynamic(property_id=property_id, dynamic_info=dynamic_info)
    
    def delete_open_house_event_dynamic_by_property(self, property_id: int) -> bool:
        if not property_id:
            return False
        redis_client = get_redis_client()
        result = redis_client.delete(f"property_id:{property_id}:dynamic_info")
        return bool(result)
    
    def create_open_house_event_dynamic(self, property_id:int, dynamic_info:DynamicInfo) -> bool:
        if not property_id:
            return False
        if not dynamic_info:
            return False
        redis_client = get_redis_client()
        data = {
            "date": dynamic_info.date,
            "time": dynamic_info.time
        }
        result = redis_client.set(f"property_id:{property_id}:dynamic_info", json.dumps(data))
        return bool(result)
    
    def update_open_house_event_dynamic(self, property_id:int = None, dynamic_info:DynamicInfo = None) -> bool:
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:dynamic_info")
        if not raw_data:
            return False
        data = json.loads(raw_data)
        if dynamic_info.date:
            data["date"] = dynamic_info.date
        if dynamic_info.time:
            data["time"] = dynamic_info.time
        result = redis_client.set(f"property_id:{property_id}:dynamic_info", json.dumps(data))
        return bool(result)
    
    # when the ttl of the key expires, the event is considered closed and another dynamic event is created, updating the date of the previous event
    # oss: open house event static is needed for the operation (time_schedule is needed)

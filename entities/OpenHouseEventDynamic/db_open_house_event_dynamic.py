import json
from entities.OpenHouseEventDynamic.open_house_event_dynamic import OpenHouseEventDynamic, DynamicInfo
from setup.redis_setup.redis_setup import get_redis_client

class OpenHouseEventDynamicDB:
    open_house_event_dynamic:OpenHouseEventDynamic = None
    
    def __init__(self, open_house_event_dynamic:OpenHouseEventDynamic):
        self.open_house_event_dynamic = open_house_event_dynamic
    
    def get_open_house_event_dynamic_by_property(self, property_id:int) -> OpenHouseEventDynamic:
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"dynamic_info:{property_id}")
        if not raw_data:
            return None
        data = json.loads(raw_data)
        dynamic_info = DynamicInfo(
            event_id=data["event_id"],
            date=data["date"],
            time=data["time"]
        )
        return OpenHouseEventDynamic(property_id=property_id, dynamic_info=dynamic_info)
    
    def delete_open_house_event_dynamic_by_property(self, property_id: int) -> bool:
        redis_client = get_redis_client()
        result = redis_client.delete(f"dynamic_info:{property_id}")
        return bool(result)
        
    # todo: implement the following methods
    # create open house event (new property inserted in mongo)
    # update open house event (open house date and time updated in mongo) -> mabye notify the buyers about the change
    # delete open house event (property deleted in mongo) -> also delete all the reservations related to this property
    # update open house event when the event occurs -> also delete all the reservations related to this property for this event
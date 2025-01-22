import json
from entities.OpenHouseEventStatic.open_house_event_static import OpenHouseEventStatic, StaticInfo
from setup.redis_setup.redis_setup import get_redis_client

class OpenHouseEventStaticDB:
    open_house_event_static:OpenHouseEventStatic = None
    
    def __init__(self, open_house_event_static:OpenHouseEventStatic):
        self.open_house_event_static = open_house_event_static
    
    def get_open_house_event_static_by_property(self, property_id:int) -> OpenHouseEventStatic:
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
            address=data["address"]
        )
        return OpenHouseEventStatic(property_id=property_id, static_info=static_info)
   
    def delete_open_house_event_static_by_property(self, property_id: int) -> bool:
        redis_client = get_redis_client()
        result = redis_client.delete(f"static_info:{property_id}")
        return bool(result)

    # todo: implement the following methods
    # create open house event (new property inserted in mongo)
    # update open house event (property updated in mongo)
    # delete open house event (property deleted in mongo) -> also delete all the reservations related to this property
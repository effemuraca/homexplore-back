from entities.OpenHouseEventDynamic.open_house_event_dynamic import OpenHouseEventDynamic
from setup.redis_setup.redis_setup import get_redis_client

class OpenHouseEventDynamicDB:
    open_house_event_dynamic:OpenHouseEventDynamic = None
    
    def __init__(self, open_house_event_dynamic:OpenHouseEventDynamic):
        self.open_house_event_dynamic = open_house_event_dynamic
    
    def get_open_house_event_dynamic_by_attribute(self, attribute:str):
        redis_client = get_redis_client()
        
    
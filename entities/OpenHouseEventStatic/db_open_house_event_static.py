from entities.OpenHouseEventStatic.open_house_event_static import OpenHouseEventStatic
from setup.redis_setup.redis_setup import get_redis_client

class OpenHouseEventStaticDB:
    open_house_event_static:OpenHouseEventStatic = None
    
    def __init__(self, open_house_event_static:OpenHouseEventStatic):
        self.open_house_event_static = open_house_event_static
    
    def get_open_house_event_static_by_attribute(self, attribute:str):
        redis_client = get_redis_client()
        
    
import json
from entities.OpenHouseEvent.open_house_event import OpenHouseEvent, OpenHouseInfo
from setup.redis_setup.redis_setup import get_redis_client

class OpenHouseEventDB:
    open_house_event:OpenHouseEvent = None
    
    def __init__(self, open_house_event:OpenHouseEvent):
        self.open_house_event = open_house_event
    
    def get_open_house_event_by_property(self, property_id:int) -> OpenHouseEvent:
        if not property_id:
            return None
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:open_house_info")
        if not raw_data:
            return None
        data = json.loads(raw_data)
        open_house_info = OpenHouseInfo(
            date=data["date"],
            time=data["time"],
            max_attendees=data["max_attendees"],
            attendees=data["attendees"]
        )
        return OpenHouseEvent(property_id=property_id, open_house_info=open_house_info)
    
    def delete_open_house_event_by_property(self, property_id: int) -> bool:
        if not property_id:
            return False
        redis_client = get_redis_client()
        result = redis_client.delete(f"property_id:{property_id}:open_house_info")
        return bool(result)
    
    def create_open_house_event(self, property_id:int, open_house_info:OpenHouseInfo) -> bool:
        if not property_id:
            return False
        if not open_house_info:
            return False
        redis_client = get_redis_client()
        data = {
            "date": open_house_info.date,
            "time": open_house_info.time,
            "max_attendees": open_house_info.max_attendees,
            "attendees": open_house_info.attendees
        }
        result = redis_client.set(f"property_id:{property_id}:open_house_info", json.dumps(data))
        return bool(result)
    
    def update_open_house_event(self, property_id:int = None, open_house_info:OpenHouseInfo = None) -> bool:
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:open_house_info")
        if not raw_data:
            return False
        data = json.loads(raw_data)
        if open_house_info.date:
            data["date"] = open_house_info.date
        if open_house_info.time:
            data["time"] = open_house_info.time
        if open_house_info.max_attendees:
            data["max_attendees"] = open_house_info.max_attendees
        if open_house_info.attendees:
            data["attendees"] = open_house_info.attendees
        result = redis_client.set(f"property_id:{property_id}:open_house_info", json.dumps(data))
        return bool(result)
    
    def increment_attendees(self, property_id:int) -> bool:
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:open_house_info")
        if not raw_data:
            return False
        data = json.loads(raw_data)
        if data["attendees"] == data["max_attendees"]:
            return False
        data["attendees"] += 1
        result = redis_client.set(f"property_id:{property_id}:open_house_info", json.dumps(data))
        return bool(result)
    
    # this method is used to decrement the number of attendees when a reservation is canceled or when an insert is not successful
    def decrement_attendees(self, property_id:int) -> bool:
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:open_house_info")
        if not raw_data:
            return False
        data = json.loads(raw_data)
        if data["attendees"] == 0:
            return False
        data["attendees"] -= 1
        result = redis_client.set(f"property_id:{property_id}:open_house_info", json.dumps(data))
        return bool(result)
     
    # when the ttl of the key expires, the event is considered closed and another dynamic event is created, updating the date of the previous event
    
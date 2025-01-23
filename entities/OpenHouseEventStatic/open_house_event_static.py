class StaticInfo:
    event_id:int = None
    thumbnail:str = None
    type:str = None
    price:int = None
    address:str = None
    time_schedule:str = None

    def __init__(self, event_id:int, thumbnail:str, type:str, price:int, address:str, time_schedule:str):
        self.event_id = event_id
        self.thumbnail = thumbnail
        self.type = type
        self.price = price
        self.address = address
        self.time_schedule = time_schedule
    

class OpenHouseEventStatic:
    property_id:int = None
    static_info:str = None
    
    def __init__(self, property_id:int, static_info:StaticInfo):
        self.property_id = property_id
        self.static_info = static_info
        
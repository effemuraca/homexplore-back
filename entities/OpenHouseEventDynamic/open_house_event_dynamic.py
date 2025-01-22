class DynamicInfo:
    event_id:int = None
    date:str = None
    time:str = None

    def __init__(self, event_id:int, date:str, time:str):
        self.event_id = event_id
        self.date = date
        self.time = time
    

class OpenHouseEventDynamic:
    property_id:int = None
    dynamic_info:str = None
    
    def __init__(self, property_id:int, dynamic_info:DynamicInfo):
        self.property_id = property_id
        self.dynamic_info = dynamic_info
        
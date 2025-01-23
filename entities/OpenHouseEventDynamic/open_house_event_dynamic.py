class DynamicInfo:
    date:str = None
    time:str = None

    def __init__(self, date:str, time:str):
        self.date = date
        self.time = time
        

class OpenHouseEventDynamic:
    property_id:int = None
    dynamic_info:DynamicInfo = None
    
    def __init__(self, property_id:int, dynamic_info:DynamicInfo):
        self.property_id = property_id
        self.dynamic_info = dynamic_info
        
    # this entity is related to:
    # - A property is created -> I need to create a new open house event
    # - The date/time of the open house event is updated -> I need to update the open house event
    # - A property is removed -> I need to remove the open house event
    # - A new reservation is made by a buyer -> I need to store his info in the reservations list


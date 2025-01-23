class StaticInfo:
    thumbnail:str = None
    property_type:str = None
    price:int = None
    address:str = None
    time_schedule:str = None

    def __init__(self, thumbnail:str, property_type:str, price:int, address:str, time_schedule:str):
        self.thumbnail = thumbnail
        self.property_type = property_type
        self.price = price
        self.address = address
        self.time_schedule = time_schedule
    

class OpenHouseEventStatic:
    property_id:int = None
    static_info:StaticInfo = None
    
    def __init__(self, property_id:int, static_info:StaticInfo):
        self.property_id = property_id
        self.static_info = static_info

    # this entity is related to:
    # - A property is created -> I need to create a new open house event
    # - A property is updated -> I need to update the open house event
    # - A property is removed -> I need to remove the open house event
    # - A new reservation is made by a buyer -> I need to store his info in the reservations list
    # - A reservation is canceled by a buyer -> I need to remove his info from the reservations list

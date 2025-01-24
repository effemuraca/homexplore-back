from pydantic import BaseModel
from typing import Optional, List
class OpenHouseInfo(BaseModel):
    date: Optional[str] = None
    time: Optional[str] = None
    max_attendees: Optional[int] = None
    attendees: Optional[int] = None

    def __init__(
        self, 
        date:str = None, 
        time:str = None, 
        max_attendees:int = None, 
        attendees:int = None
    ):
        super().__init__()
        self.date = date
        self.time = time
        self.max_attendees = max_attendees
        self.attendees = attendees

        

class OpenHouseEvent(BaseModel):
    property_id: Optional[int] = None
    open_house_info: Optional[OpenHouseInfo] = None
    
    def __init__(
        self, 
        property_id:int = None, 
        open_house_info:OpenHouseInfo = None
    ):
        super().__init__()
        self.property_id = property_id
        self.open_house_info = open_house_info
        
    # this entity is related to:
    # - A property is created -> I need to create a new open house event
    # - A property is updated -> I need to update the open house event
    # - A property is removed -> I need to remove the open house event
    # - A new reservation is made by a buyer -> I need to store his info in the reservations list
    # - A reservation is canceled by a buyer -> I need to remove his info from the reservations list
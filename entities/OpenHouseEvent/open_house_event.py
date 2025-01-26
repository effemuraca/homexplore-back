from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
class OpenHouseInfo(BaseModel):
    date: Optional[str] = None
    time: Optional[str] = None
    max_attendees: Optional[int] = None
    attendees: Optional[int] = None

    def __init__(
        self, 
        date:str = None, 
        time:str = None, 
        area:int = None, 
    ):
        super().__init__()
        self.date = date
        self.time = time
        # the area of the property determines the max number of attendees
        # 10 sqft per attendee, with respect to american fire prevention standards
        self.max_attendees = area / 10 if area else 0
        self.attendees = 0

        

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

    def date_and_time_to_seconds(self) -> int:
        date = self.open_house_info.date
        time = self.open_house_info.time
        date_time = f"{date} {time}"
        return int(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timestamp())

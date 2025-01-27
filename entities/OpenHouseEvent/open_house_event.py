from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class OpenHouseInfo(BaseModel):
    date: Optional[str] = Field(None, example="2023-10-01")
    time: Optional[str] = Field(None, example="14:00:00")
    max_attendees: Optional[int] = Field(0, example=50)
    attendees: Optional[int] = Field(0, example=30)

    def __init__(
        __pydantic_self__,
        date: Optional[str] = None,
        time: Optional[str] = None,
        max_attendees: Optional[int] = 0,
        attendees: Optional[int] = 0,
        area: Optional[int] = None
    ):
        if area is not None:
            # max_attendees is calculated following the fire regulation of 1 person every 10 sqft
            max_attendees = area // 10
        super().__init__(
            date=date,
            time=time,
            max_attendees=max_attendees,
            attendees=attendees
        )

class OpenHouseEvent(BaseModel):
    property_id: Optional[int] = Field(None, example=1)
    open_house_info: Optional[OpenHouseInfo] = None

    def date_and_time_to_seconds(self) -> int:
        """
        Converts date + time to epoch seconds. Expected format: YYYY-MM-DD HH:MM:SS.
        """
        if not self.open_house_info or not self.open_house_info.date or not self.open_house_info.time:
            return 0
        try:
            date_time = f"{self.open_house_info.date} {self.open_house_info.time}"
            return int(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timestamp())
        except ValueError:
            return 0
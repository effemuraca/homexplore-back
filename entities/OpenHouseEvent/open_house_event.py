from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OpenHouseInfo(BaseModel):
    date: Optional[str] = None
    time: Optional[str] = None
    max_attendees: Optional[int] = 0
    attendees: Optional[int] = 0

    def __init__(
        __pydantic_self__,
        date: Optional[str] = None,
        time: Optional[str] = None,
        max_attendees: Optional[int] = 0,
        attendees: Optional[int] = 0,
        area: Optional[int] = None
    ):
        # Se 'area' è presente, calcoliamo automaticamente max_attendees
        if area is not None:
            max_attendees = area // 10
        super().__init__(
            date=date,
            time=time,
            max_attendees=max_attendees,
            attendees=attendees
        )

class OpenHouseEvent(BaseModel):
    property_id: Optional[int] = None
    open_house_info: Optional[OpenHouseInfo] = None

    def date_and_time_to_seconds(self) -> int:
        """
        Converte date + time in secondi. Formato atteso: YYYY-MM-DD HH:MM:SS.
        """
        if not self.open_house_info or not self.open_house_info.date or not self.open_house_info.time:
            return 0
        date_time = f"{self.open_house_info.date} {self.open_house_info.time}"
        return int(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timestamp())
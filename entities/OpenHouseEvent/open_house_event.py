from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class OpenHouseInfo(BaseModel):
    day: Optional[str] = Field(None, example="Monday")
    start_time: Optional[str] = Field(None, example="10:00 AM")
    max_attendees: Optional[int] = Field(0, example=50)
    attendees: int = Field(0, example=0) 

    def __init__(
        __pydantic_self__,
        day: Optional[str] = None,
        start_time: Optional[str] = None,
        max_attendees: Optional[int] = 0,
        area: Optional[int] = None,
    ):
        if area is not None:
            # max_attendees è calcolato secondo la normativa antincendio: 1 persona ogni 10 sqft
            max_attendees = area // 10
        super().__init__(
            day = day,
            start_time = start_time,
            max_attendees = max_attendees,
            attendees = 0  
        )
    
def convert_to_seconds(self) -> Optional[int]:
        """
        Converts the day and time to the number of seconds from now to the specified date and time.
        Returns None if the 'day' or 'start_time' fields are invalid.
        """
        try:
            if not self.day or not self.start_time:
                logger.error("Missing 'day' or 'start_time' field.")
                return None

            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            day = self.day.capitalize()
            
            if day not in days:
                logger.error(f"Invalid day: {day}")
                return None

            day_index = days.index(day)
            today = datetime.now()
            current_weekday = today.weekday()  # Monday is 0

            days_ahead = day_index - current_weekday
            if days_ahead < 0:
                days_ahead += 7  # Move to the next week

            event_date = today + timedelta(days=days_ahead)
            
            # Handle time format "HH:MM AM/PM"
            time_parts = self.start_time.strip().split(" ")
            if len(time_parts) != 2:
                logger.error(f"Invalid time format: {self.start_time}")
                return None

            time_str, period = time_parts
            hour_minute = time_str.split(":")
            if len(hour_minute) != 2:
                logger.error(f"Invalid time format: {self.start_time}")
                return None

            hour = int(hour_minute[0])
            minute = int(hour_minute[1])

            if period.upper() == "PM" and hour != 12:
                hour += 12
            elif period.upper() == "AM" and hour == 12:
                hour = 0

            event_datetime = event_date.replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0
            )

            # Calculate the difference in seconds from now to the event time
            time_delta = event_datetime - today
            total_seconds = int(time_delta.total_seconds())

            if total_seconds < 0:
                logger.error("Event time is in the past.")
                return None

            return total_seconds

        except Exception as e:
            logger.error(f"Error converting to seconds: {e}")
            return None

class OpenHouseEvent(BaseModel):
    property_id: Optional[int] = Field(None, example=1)
    open_house_info: Optional[OpenHouseInfo] = None

# Test the convert_to_seconds method

# Create an OpenHouseInfo object
open_house_info = OpenHouseInfo(
    day="Monday",
    start_time="10:00 AM",
    area=1000
)
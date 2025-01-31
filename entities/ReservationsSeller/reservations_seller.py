from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)
class ReservationS(BaseModel):
    buyer_id: Optional[str] = Field(None, example=1)
    full_name: Optional[str] = Field(None, example="John Doe")
    email: Optional[str] = Field(None, example="john@example.com")
    phone: Optional[str] = Field(None, example="1234567890")

class ReservationsSeller(BaseModel):
    property_id: Optional[str] = Field(None, example=1)
    reservations: Optional[List[ReservationS]] = None
    max_reservations: Optional[int] = Field(0, example=50)
    total_reservations: Optional[int] = Field(0, example=0)

    def __init__(
        __pydantic_self__,
        property_id: Optional[str] = None,
        reservations: Optional[List[ReservationS]] = None,
        area: Optional[int] = 0,
        total_reservations: Optional[int] = 0
    ):
        super().__init__(
            property_id = property_id,
            reservations = reservations,
            max_reservations = ReservationsSeller.calculate_max_reservations(area),
            total_reservations = total_reservations
        )

    @staticmethod
    def calculate_max_reservations(area: int) -> int:
        """
        Calculates the maximum number of reservations based on the provided area.
        """
        return area // 10  # 1 person per 10 sqft
    
def convert_to_seconds(day : str, start_time : str) -> Optional[int]:
    """
    Converts the day and time to the number of seconds from now to the specified date and time.
    Returns None if the 'day' or 'start_time' fields are invalid.
    """
    try:
        if not day or not start_time:
            logger.error("Missing 'day' or 'start_time' field.")
            return None
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day = day.capitalize()
        if day not in days:
            logger.error(f"Invalid day: {day}")
            return None
        day_index = days.index(day)
        today = datetime.now()
        current_weekday = today.weekday()
        days_ahead = day_index - current_weekday
        if days_ahead < 0:
            days_ahead += 7
        event_date = today + timedelta(days=days_ahead)
        time_parts = start_time.strip().split(" ")
        if len(time_parts) != 2:
            logger.error(f"Invalid time format: {start_time}")
            return None
        time_str, period = time_parts
        hour_minute = time_str.split(":")
        if len(hour_minute) != 2:
            logger.error(f"Invalid time format: {start_time}")
            return None
        hour = int(hour_minute[0])
        minute = int(hour_minute[1])
        if period.upper() == "PM" and hour != 12:
            hour += 12
        elif period.upper() == "AM" and hour == 12:
            hour = 0
        event_datetime = event_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        total_seconds = int((event_datetime - today).total_seconds())
        if total_seconds < 0:
            logger.error("Event time is in the past.")
            return None
        return total_seconds
    except Exception as e:
        logger.error(f"Error converting to seconds: {e}")
        return None
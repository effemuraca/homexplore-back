from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional, List
from datetime import datetime, timedelta
from bson import ObjectId

class ReservationS(BaseModel):
    buyer_id: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    
    @field_validator('buyer_id')
    def check_object_id(cls, v: str) -> str:
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId string')
        return v

class ReservationsSeller(BaseModel):
    property_on_sale_id: Optional[str] = None
    reservations: Optional[List[ReservationS]] = []
    
    @field_validator('property_on_sale_id')
    def check_object_id(cls, v: str) -> str:
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId string')
        return v

    def __init__(
        self,
        property_on_sale_id: Optional[str] = None,
        reservations: Optional[List[ReservationS]] = None,
    ):
        reservations = reservations or []
        super().__init__(
            property_on_sale_id=property_on_sale_id,
            reservations=reservations
        )

def convert_to_seconds(day: str, time: str) -> Optional[int]:
    """
    Convert a day and a time interval (e.g. "10:00 AM - 11:00 AM") to seconds from now,
    using only the end time of the interval.
    """
    try:
        if not day or not time:
            return None
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day = day.capitalize()
        if day not in days:
            return None
        
        day_index = days.index(day)
        today = datetime.now()
        current_weekday = today.weekday()
        days_ahead = day_index - current_weekday
        if days_ahead < 0:
            days_ahead += 7
        event_date = today + timedelta(days=days_ahead)
        
        time_parts = time.split("-")
        if len(time_parts) != 2:
            return None
        end_time_str = time_parts[1].strip()
        
        time_obj = datetime.strptime(end_time_str, "%I:%M %p")
        event_datetime = datetime.combine(event_date.date(), time_obj.time())
        
        delta = (event_datetime - today).total_seconds()
        if delta <= 0:
            event_datetime += timedelta(days=7)
            delta = (event_datetime - today).total_seconds()
            
        return int(delta)
    except Exception:
        return None

def next_weekday(target_day: str) -> Optional[str]:
    days = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }
    target_day_lower = target_day.lower()
    if target_day_lower not in days:
        return None
    today = datetime.now()
    today_weekday = today.weekday()
    target_weekday = days[target_day_lower]
    days_ahead = target_weekday - today_weekday
    if days_ahead <= 0:
        days_ahead += 7
    next_day = today + timedelta(days=days_ahead)
    return next_day.strftime("%Y-%m-%d")
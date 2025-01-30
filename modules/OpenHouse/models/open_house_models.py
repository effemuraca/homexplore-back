from pydantic import BaseModel, Field
from typing import Optional


class CreateOpenHouseEvent(BaseModel):
    property_id : str = Field(example="615c44fdf641be001f0c1111")
    day: str = Field(example="Monday")
    start_time: str = Field(example="10:00 AM")
    max_attendees: int = Field(example=50)
    area: int = Field(example=500)
  

class UpdateOpenHouseEvent(BaseModel):
    property_id : str = Field(example="615c44fdf641be001f0c1111")
    day: Optional[str] = Field(None, example="Monday")
    start_time: Optional[str] = Field(None, example="10:00 AM")
    max_attendees: Optional[int] = Field(None, example=50)
    area: Optional[int] = Field(None, example=500)
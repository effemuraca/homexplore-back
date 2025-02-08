import re
from typing import Any
from pydantic import BaseModel, field_validator

class Neo4jPoint(BaseModel):
    latitude: float
    longitude: float

    @field_validator('latitude')
    def check_latitude(cls, v):
        if not (-90 <= v <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        return v

    @field_validator('longitude')
    def check_longitude(cls, v):
        if not (-180 <= v <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return v

class City(BaseModel):
    name: str
    coordinates: Neo4jPoint
    safety_index: float
    health_care_index: float
    cost_of_living_index: float
    pollution_index: float

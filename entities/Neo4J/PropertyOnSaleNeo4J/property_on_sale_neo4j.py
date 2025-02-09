from pydantic import BaseModel, field_validator
from neo4j.spatial import Point
from typing import Optional, Any

class Neo4jPoint(BaseModel):
    latitude: float
    longitude: float
    
    @field_validator('latitude')
    def check_latitude(cls, v):
        if not (-90 <= v <= 90):
            raise ValueError("Latitude must be between -90 e 90")
        return v

    @field_validator('longitude')
    def check_longitude(cls, v):
        if not (-180 <= v <= 180):
            raise ValueError("Longitude must be between -180 e 180")
        return v

class PropertyOnSaleNeo4J(BaseModel):
    property_on_sale_id: Optional[str] = None
    coordinates: Optional[Neo4jPoint] = None
    price: Optional[int] = None
    type: Optional[str] = None
    thumbnail: Optional[str] = None
    score: Optional[float] = None
    
    @field_validator('property_on_sale_id')
    def check_object_id(cls, v: str) -> str:
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId string')
        return v
    
    @field_validator('thumbnail')
    def validate_thumbnail(cls, v: str) -> str:
        if not re.match(r'^https?://.*\.(?:png|jpg|jpeg|gif)$', v):
            raise ValueError('Invalid URL format.')
        return v
    
    @field_validator('price')
    def validate_price(cls, v: int) -> int:
        if v < 0:
            raise ValueError('Price must be positive.')
        return v
    
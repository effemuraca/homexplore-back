from pydantic import BaseModel, Field, validator
from typing import Optional

class Analytics1Input(BaseModel):
    city: str = Field(example="New York")
    type: Optional[str] = Field(None, example="condo")
    order_by: Optional[int] = Field(1, example="decreasing")

   #check if the type is a "condo" or other type of house using validator
    @validator("type")
    def validate_type(cls, value):
        valid_types = {"condo", "house", "apartment"}
        if value not in valid_types:
            raise ValueError("Invalid type. Must be one of: " + ", ".join(valid_types))
        return value

    #check if the order_by is 1 or -1 using validator
    @validator("order_by")
    def validate_order_by(cls, value):
        if value not in {1, -1}:
            raise ValueError("Invalid order_by. Must be 1 or -1")
        return value

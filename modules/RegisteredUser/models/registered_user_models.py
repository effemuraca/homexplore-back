from pydantic import BaseModel, Field, field_validator
from typing import Optional

class Analytics1Input(BaseModel):
    city: str = Field(example="New York")
    type: Optional[str] = Field(None, example="condo")
    order_by: Optional[int] = Field(1, example="decreasing")

    @field_validator("order_by")
    def validate_order_by(cls, value):
        if value not in {1, -1}:
            raise ValueError("Invalid order_by. Must be 1 or -1")
        return value

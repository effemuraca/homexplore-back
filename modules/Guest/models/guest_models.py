from pydantic import BaseModel, Field, validator
from typing import Optional


class FilteredSearchInput(BaseModel):
    city: Optional[str] = Field(None, example="New York")
    neighbourhood: Optional[str] = Field(None, example="Brooklyn")
    max_price: Optional[int] = Field(None, example=500000)
    type: Optional[str] = Field(None, example="House")
    min_area: Optional[int] = Field(None, example=2000)
    min_bed_number: Optional[int] = Field(None, example=3)
    min_bath_number: Optional[int] = Field(None, example=2)

    #check type of property is in a range of value using validator
    @validator("type")
    def validate_type(cls, value):
        valid_types = {"House", "Apartment", "Condo"}
        if value not in valid_types:
            raise ValueError("Invalid type. Must be one of: " + ", ".join(valid_types))
        return value
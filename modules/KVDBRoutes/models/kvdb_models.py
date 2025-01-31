from pydantic import BaseModel, Field
from typing import Optional, List

class SuccessModel(BaseModel):
    detail: str

class ErrorModel(BaseModel):
    detail: str

class BookNow(BaseModel):
    buyer_id: str = Field(example="615c44fdf641be001f0c1111")
    property_id: str = Field(example="615c44fdf641be001f0c1111")
    date: str = Field(example="2021-09-01")
    time: str = Field(example="10:00")
    thumbnail: str = Field(example="https://www.example.com/image")
    address: str = Field(example="1234 Example St.")
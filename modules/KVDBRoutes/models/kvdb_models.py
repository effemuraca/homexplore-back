from pydantic import BaseModel
from typing import Optional, List

class SuccessModel(BaseModel):
    detail: str

class ErrorModel(BaseModel):
    detail: str
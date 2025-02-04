from pydantic import BaseModel
from typing import List

class SuccessModel(BaseModel):
    detail: str

class ErrorModel(BaseModel):
    detail: str

class Analtyrics1ResponseModel(BaseModel):
    detail: str
    result: List[dict]

Analytics1Responses = {
    200: {
        "model": Analtyrics1ResponseModel,
        "description": "Analytics data retrieved successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Aggregated data finished successfully",
                    "result": [
                        {
                            "_id": "Brooklyn",
                            "avg_price": 2300.5
                        },
                        {
                            "_id": "Manhattan",
                            "avg_price": 2500.5
                        }
                    ]
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Database client not found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Database client not found"
                }
            }
        }
    }
}
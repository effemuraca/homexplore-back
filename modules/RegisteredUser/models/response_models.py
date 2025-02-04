from pydantic import BaseModel
from typing import List

class SuccessModel(BaseModel):
    detail: str

class ErrorModel(BaseModel):
    detail: str

class AnalyticsResponseModel(BaseModel):
    detail: str
    result: List[dict]

Analytics1Responses = {
    200: {
        "model": AnalyticsResponseModel,
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

Analytics4Responses = {
    200: {
        "model": AnalyticsResponseModel,
        "description": "Analytics data retrieved successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Aggregated data finished successfully",
                    "result": [
                        {
                            "_id": "Condo",
                            "avg_price": 2300.5
                        },
                        {
                            "_id": "House",
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

Analytics5Responses = {
    200: {
        "model": AnalyticsResponseModel,
        "description": "Analytics data retrieved successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Aggregated data finished successfully",
                    "result": [
                        {
                            "_id": "Condo",
                            "avg_bed_number": 2.5,
                            "avg_bath_number": 1.5,
                            "avg_area": 2000
                        },
                        {
                            "_id": "House",
                            "avg_bed_number": 3.5,
                            "avg_bath_number": 2.5,
                            "avg_area": 2500
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
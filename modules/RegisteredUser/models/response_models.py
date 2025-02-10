from pydantic import BaseModel
from typing import List

class SuccessModel(BaseModel):
    detail: str

class ErrorModel(BaseModel):
    detail: str


class GroupedNeighbourhoodResponseModel(BaseModel):
    avg_price: float
    neighbourhood: str
class Analytics1ResponseModel(BaseModel):
    detail: str
    result: List[GroupedNeighbourhoodResponseModel]

Analytics1Responses = {
    200: {
        "model": Analytics1ResponseModel,
        "description": "Analytics data retrieved successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Aggregated data finished successfully",
                    "result": [
                        {
                            "neighbourhood": "Brooklyn",
                            "avg_price": 2300.5
                        },
                        {
                            "neighbourhood": "Manhattan",
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

class GroupedPropertiesResponseModel(BaseModel):
    avg_price: float
    count: int
    type: str

class Analytics4ResponseModel(BaseModel):
    detail: str
    result: List[GroupedPropertiesResponseModel]
    
Analytics4Responses = {
    200: {
        "model": Analytics4ResponseModel,
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

class GroupedPropertiesWithAreaResponseModel(BaseModel):
    avg_bed_number: float
    avg_bath_number: float
    avg_area: float
    type: str

class Analytics5ResponseModel(BaseModel):
    detail: str
    result: List[GroupedPropertiesWithAreaResponseModel]


Analytics5Responses = {
    200: {
        "model": Analytics5ResponseModel,
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
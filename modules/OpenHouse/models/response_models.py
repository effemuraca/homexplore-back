from pydantic import BaseModel
from entities.OpenHouseEvent.open_house_event import OpenHouseEvent

class SuccessModel(BaseModel):
    detail: str

class ErrorModel(BaseModel):
    detail: str

GetOpenHouseEventResponseModelResponses = {
    200: {
        "model": OpenHouseEvent,
        "description": "Open house event data retrieved successfully.",
        "content": {
            "application/json": {
                "example": {
                    "property_id": "615c44fdf641be001f0c1111",
                    "open_house_info": {
                        "max_attendees": 50,
                        "attendees": 0
                    }
                }
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "Open house event not found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Open house event not found"
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Error retrieving open house event.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Error retrieving open house event"
                }
            }
        }
    }
}

CreateOpenHouseEventResponseModelResponses = {
    201: {
        "model": SuccessModel,
        "description": "Successful operation, returns a success message.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Open house event created"
                }
            }
        }
    },
    
    500: {
        "model": ErrorModel,
        "description": "Error creating open house event.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Error creating open house event"
                }
            }
        }
    }
}

DeleteOpenHouseEventResponseModelResponses = {
    200: {
        "model": SuccessModel,
        "description": "Successful operation, returns a success message.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Open house event deleted"
                }
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "Open house event not found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Open house event not found"
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Error deleting open house event.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Error deleting open house event"
                }
            }
        }
    }
}

UpdateOpenHouseEventResponseModelResponses = {
    200: {
        "model": SuccessModel,
        "description": "Successful operation, returns a success message.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Open house event updated"
                }
            }
        }
    },
    400: {
        "model": ErrorModel,
        "description": "Invalid day or time.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid day or time"
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Error updating open house event.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Error updating open house event"
                }
            }
        }
    }
}
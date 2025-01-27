from pydantic import BaseModel
from entities.OpenHouseEvent.open_house_event import OpenHouseEvent

class SuccessModel(BaseModel):
    detail: str

class ErrorModel(BaseModel):
    detail: str

OpenHouseEventResponseModelResponses = {
    200: {
        "model": OpenHouseEvent,
        "description": "Successful operation, returns the open house event details.",
        "content": {
            "application/json": {
                "example": {
                    "property_id": 1,
                    "open_house_info": {
                        "date": "2023-10-01",
                        "time": "14:00:00",
                        "max_attendees": 50,
                        "attendees": 30
                    }
                }
            }
        }
    },
    401: {
        "model": ErrorModel,
        "description": "User not authenticated.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "User not authenticated"
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
    401: {
        "model": ErrorModel,
        "description": "User not authenticated.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "User not authenticated"
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
    401: {
        "model": ErrorModel,
        "description": "User not authenticated.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "User not authenticated"
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
    401: {
        "model": ErrorModel,
        "description": "User not authenticated.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "User not authenticated"
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
from pydantic import BaseModel
from entities.ReservationsBuyer.reservations_buyer import ReservationsBuyer

class SuccessModel(BaseModel):
    detail: str

class ErrorModel(BaseModel):
    detail: str


ReservationDeletedResponses = {
    200: {
        "model": SuccessModel,
        "description": "Reservation deleted successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Reservation deleted successfully."
                }
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "Reservation not found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Reservation not found."
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Failed to delete reservation.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Failed to delete reservation."
                }
            }
        }
    }
}

BookNowResponses = {
    200: {
        "model": SuccessModel,
        "description": "Reservation created successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Reservation created successfully."
                }
            }
        }
    },
    400: {
        "model": ErrorModel,
        "description": "Invalid input provided.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid day provided."
                }
            }
        }
    },
    409: {
        "model": ErrorModel,
        "description": "Reservation already exists.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Reservation already exists."
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Internal server error.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Internal server error."
                }
            }
        }
    }
}
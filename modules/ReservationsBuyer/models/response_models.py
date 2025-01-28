from pydantic import BaseModel
from typing import Dict, Any
from entities.ReservationsBuyer.reservations_buyer import ReservationsBuyer

class SuccessModel(BaseModel):
    detail: str

class ErrorModel(BaseModel):
    detail: str

ReservationsBuyerResponseModelResponses: Dict[int, Dict[str, Any]] = {
    200: {
        "model": ReservationsBuyer,
        "description": "Successful operation, returns the reservations list.",
        "content": {
            "application/json": {
                "example": {
                    "buyer_id": 1,
                    "reservations": [
                        {
                            "property_id": 1,
                            "date": "2021-09-01",
                            "time": "10:00",
                            "thumbnail": "https://www.example.com/image.jpg",
                            "address": "1234 Example St."
                        }
                    ]
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
        "description": "No reservations found for this user.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "No reservations found"
                }
            }
        }
    }
}

CreateReservationsBuyerResponseModelResponses: Dict[int, Dict[str, Any]] = {
    201: {
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
        "description": "Invalid input or missing reservation info.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid reservation info."
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Failed to create reservation.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Failed to create reservation."
                }
            }
        }
    }
}

DeleteReservationsBuyerResponseModelResponses: Dict[int, Dict[str, Any]] = {
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
        "description": "Reservation not found or delete failed.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Reservation not found or delete failed."
                }
            }
        }
    }
}

UpdateReservationsBuyerResponseModelResponses: Dict[int, Dict[str, Any]] = {
    200: {
        "model": ReservationsBuyer,
        "description": "Reservation updated successfully.",
        "content": {
            "application/json": {
                "example": {
                    "buyer_id": 1,
                    "reservations": [
                        {
                            "property_id": 1,
                            "date": "2021-09-02",
                            "time": "11:00",
                            "thumbnail": "https://www.example.com/new_image.jpg",
                            "address": "5678 Example Ave."
                        }
                    ]
                }
            }
        }
    },
    400: {
        "model": ErrorModel,
        "description": "Invalid input or missing reservation info.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid reservation info."
                }
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "Reservation not found or update failed.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Reservation not found or update failed."
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Failed to update reservation.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Failed to update reservation."
                }
            }
        }
    }
}
from pydantic import BaseModel
from typing import Dict, Any
from entities.ReservationsSeller.reservations_seller import ReservationsSeller

class SuccessModel(BaseModel):
    detail: str

class ErrorModel(BaseModel):
    detail: str

ReservationsSellerResponseModelResponses: Dict[int, Dict[str, Any]] = {
    200: {
        "model": ReservationsSeller,
        "description": "Successful operation, returns the reservations list.",
        "content": {
            "application/json": {
                "example": {
                    "property_id": 1,
                    "reservations": [
                        {
                            "user_id": 1,
                            "full_name": "John Doe",
                            "email": "john@example.com",
                            "phone": "1234567890"
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
        "description": "No reservations found for this property.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "No reservations found"
                }
            }
        }
    }
}

CreateReservationsSellerResponseModelResponses: Dict[int, Dict[str, Any]] = {
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

DeleteReservationsSellerResponseModelResponses: Dict[int, Dict[str, Any]] = {
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

UpdateReservationsSellerResponseModelResponses: Dict[int, Dict[str, Any]] = {
    200: {
        "model": ReservationsSeller,
        "description": "Reservation updated successfully.",
        "content": {
            "application/json": {
                "example": {
                    "property_id": 1,
                    "reservations": [
                        {
                            "user_id": 1,
                            "full_name": "John Doe",
                            "email": "john.new@example.com",
                            "phone": "0987654321"
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
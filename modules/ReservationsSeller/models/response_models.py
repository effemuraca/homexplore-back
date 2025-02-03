from pydantic import BaseModel
from typing import Dict, Any
from entities.Redis.ReservationsSeller.reservations_seller import ReservationsSeller

class SuccessModel(BaseModel):
    detail: str

class ErrorModel(BaseModel):
    detail: str

CreateReservationSellerResponseModelResponses: Dict[int, Dict[str, Any]] = {
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
        "description": "Invalid input provided.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid input."
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

GetReservationsSellerResponseModelResponses: Dict[int, Dict[str, Any]] = {
    200: {
        "model": ReservationsSeller,
        "description": "Reservations fetched successfully.",
        "content": {
            "application/json": {
                "example": {
                    "property_on_sale_id": "615c44fdf641be001f0c1111",
                    "reservations": [],
                    "max_reservations": 50,
                    "total_reservations": 1
                }
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "No reservations found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "No reservations found."
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Failed to fetch reservations.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Failed to fetch reservations."
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
                    "property_on_sale_id": "615c44fdf641be001f0c1111",
                    "reservations": [],
                    "max_reservations": 50,
                    "total_reservations": 2
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
                    "detail": "Invalid input."
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
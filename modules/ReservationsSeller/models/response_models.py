from pydantic import BaseModel
from entities.ReservationsSeller.reservations_seller import ReservationsSeller

class SuccessModel(BaseModel):
    detail: str

class ErrorModel(BaseModel):
    detail: str

CreateReservationSellerResponseModelResponses = {
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
    409: {
        "model": ErrorModel,
        "description": "Reservation already exists.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Reservation already exists"
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

DeleteReservationsSellerResponseModelResponses = {
    200: {
        "model": SuccessModel,
        "description": "Reservation(s) deleted successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Reservations deleted successfully."
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

GetReservationsSellerResponseModelResponses = {
    200: {
        "model": ReservationsSeller,
        "description": "Reservations retrieved successfully.",
        "content": {
            "application/json": {
                "example": {
                    "property_id": "615c44fdf641be001f0c1111",
                    "reservations": []
                }
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "No reservations found for the property.",
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
        "description": "Failed to retrieve reservations.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Failed to retrieve reservations."
                }
            }
        }
    }
}

UpdateReservationsSellerResponseModelResponses = {
    200: {
        "model": ReservationsSeller,
        "description": "Reservation updated successfully.",
        "content": {
            "application/json": {
                "example": {
                    "property_id": "615c44fdf641be001f0c1111",
                    "reservations": []
                }
            }
        }
    },
    400: {
        "model": ErrorModel,
        "description": "Invalid input.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid input data."
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
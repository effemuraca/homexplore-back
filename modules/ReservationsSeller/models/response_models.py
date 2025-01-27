from pydantic import BaseModel
from entities.ReservationsSeller.reservations_seller import ReservationsSeller

class SuccessModel(BaseModel):
    detail: str

class ErrorModel(BaseModel):
    detail: str

ReservationsSellerResponseModelResponses = {
    200: {
        "model": ReservationsSeller,
        "description": "Successful operation, returns the reservations list.",
        "content": {
            "application/json": {
                "example": {
                    "property_id": 1,
                    "reservations": [
                        {
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

CreateReservationsSellerResponseModelResponses = {
    201: {
        "model": SuccessModel,
        "description": "Successful operation, returns the created reservation.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Reservation created"
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
        "description": "Error creating reservation.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Error creating reservation"
                }
            }
        }
    }
}

DeleteReservationsSellerResponseModelResponses = {
    200: {
        "model": SuccessModel,
        "description": "Successful operation, returns the deleted reservations.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Reservations deleted"
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
        "description": "Error deleting reservations.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Error deleting reservations"
                }
            }
        }
    }
}

UpdateReservationsSellerResponseModelResponses = {
    200: {
        "model": SuccessModel,
        "description": "Successful operation, returns the updated reservation.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Reservation updated"
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
        "description": "Error updating reservation.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Error updating reservation"
                }
            }
        }
    }
}
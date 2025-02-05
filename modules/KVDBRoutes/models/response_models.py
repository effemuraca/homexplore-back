from pydantic import BaseModel
from entities.Redis.ReservationsBuyer.reservations_buyer import ReservationsBuyer

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
                    "detail": "No reservations found for buyer or seller."
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
                    "detail": "Error deleting reservation in database."
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
        "description": "Buyer already has a reservation or invalid input.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Buyer already has a reservation."
                }
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "Buyer not found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Buyer not found."
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

GetReservationsResponses = {
    200: {
        "model": ReservationsBuyer,
        "description": "Reservations retrieved successfully.",
        "content": {
            "application/json": {
                "example": {
                    "buyer_id": "example_buyer_id",
                    "reservations": [
                        {
                            "property_on_sale_id": "example_property_id",
                            "date": "2023-01-01",
                            "time": "12:00 PM",
                            "thumbnail": "https://example.com/image.jpg",
                            "address": "Example Address"
                        }
                    ]
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
        "description": "Failed to retrieve reservations.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Error retrieving reservations."
                }
            }
        }
    }
}
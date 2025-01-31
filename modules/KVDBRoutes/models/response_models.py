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
                    "buyer_reservation": {
                        "buyer_id": "1",
                        "reservations": [
                            {
                                "property_id": "1",
                                "date": "2021-09-01",
                                "time": "10:00",
                                "thumbnail": "https://www.example.com/image.jpg",
                                "address": "1234 Example St."
                            }
                        ]
                    },
                    "seller_reservation": {
                        "property_id": "1",
                        "reservations": [
                            {
                                "buyer_id": "1",
                                "full_name": "John Doe",
                                "email": "john@example.com",
                                "phone": "1234567890"
                            }
                        ]
                    },
                    "open_house_event": {
                        "property_id": "1",
                        "open_house_info": {
                            "day": "2021-09-01",
                            "start_time": "10:00",
                            "max_attendees": 100,
                            "attendees": 1,
                            "area": 50
                        }
                    },
                    "detail": "Reservation created successfully."
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
        "description": "Open house event not found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Open house event not found."
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
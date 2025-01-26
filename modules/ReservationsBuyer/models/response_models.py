# purpose:
#     this file contains the response models for this module, that are also shown in the API documentation.

from pydantic import BaseModel
from entities.ReservationsBuyer.reservations_buyer import ReservationsBuyer

class SuccessModel(BaseModel):
    detail: str

class ErrorModel(BaseModel):
    detail: str
    
ReservationsBuyerResponseModelResponses = {
    200: {
        "model": ReservationsBuyer,
        "description": "Successful operation, returns the reservations list.",
        "content": {
            "application/json": {
                "example": {
                    "user_id": 1,
                    "reservations": [
                        {
                            "property_id": 1,
                            "open_house_id": 1,
                            "date": "2021-09-01",
                            "time": "10:00",
                            "thumbnail": "https://www.example.com/image.jpg",
                            "property_type": "House",
                            "price": 1000000,
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


CreateReservationsBuyerResponseModelResponses = {
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

DeleteReservationsBuyerResponseModelResponses = {
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

UpdateReservationsBuyerResponseModelResponses = {
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


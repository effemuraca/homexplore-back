# purpose:
#     this file contains the response models for this module, that are also shown in the API documentation.

from pydantic import BaseModel
from entities.ReservationsBuyer.reservations_buyer import ReservationsBuyer
from entities.ReservationsSeller.reservations_seller import ReservationsSeller
from entities.OpenHouseEvent.open_house_event import OpenHouseEvent

#ReservationsBuyer

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

# ReservationsSeller

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

# OpenHouseEvent

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
                        "time": "14:00",
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
        "description": "Successful operation, returns the created open house event.",
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
        "description": "Successful operation, returns the deleted open house event.",
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
        "description": "Successful operation, returns the updated open house event.",
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
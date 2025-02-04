from pydantic import BaseModel
from typing import Dict, Any, List
from entities.MongoDB.Buyer.buyer import Buyer, FavouriteProperty
from entities.Redis.ReservationsBuyer.reservations_buyer import ReservationsBuyer

class SuccessModel(BaseModel):
    detail: str

class ErrorModel(BaseModel):
    detail: str

# Buyer

GetBuyerResponseModelResponses: Dict[int, Dict[str, Any]] = {
    200: {
        "model": Buyer,
        "description": "Buyer data retrieved successfully.",
        "content": {
            "application/json": {
                "example": {
                    "buyer_id": "615c44fdf641be001f0c1111",
                    "password": "hashed_password",
                    "email": "user@example.com",
                    "phone_number": "1234567890",
                    "name": "John",
                    "surname": "Doe",
                    "age": 30
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
        "description": "Buyer not found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Buyer not found"
                }
            }
        }
    }
}

class CreateBuyerResponseModel(BaseModel):
    detail: str
    buyer_id: str

CreateBuyerResponseModelResponses: Dict[int, Dict[str, Any]] = {
    201: {
        "model": SuccessModel,
        "description": "Buyer created successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Buyer created successfully."
                }
            }
        }
    },
    400: {
        "model": ErrorModel,
        "description": "Invalid input or missing buyer info.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid buyer info."
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Failed to create buyer.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Failed to create buyer."
                }
            }
        }
    }
}

UpdateBuyerResponseModelResponses: Dict[int, Dict[str, Any]] = {
    200: {
        "model": SuccessModel,
        "description": "Buyer updated successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Buyer updated successfully."
                }
            }
        }
    },
    400: {
        "model": ErrorModel,
        "description": "Invalid input or missing buyer ID.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Buyer ID is required."
                }
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "Buyer not found or update failed.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Buyer not found or update failed."
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Failed to update buyer.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Failed to update buyer."
                }
            }
        }
    }
}

DeleteBuyerResponseModelResponses: Dict[int, Dict[str, Any]] = {
    200: {
        "model": SuccessModel,
        "description": "Buyer deleted successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Buyer deleted successfully."
                }
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "Buyer not found or delete failed.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Buyer not found or delete failed."
                }
            }
        }
    }
}


# Favourites

GetFavoritesResponseModelResponses: Dict[int, Dict[str, Any]] = {
    200: {
        "model": List[FavouriteProperty],
        "description": "Favorites retrieved successfully.",
        "content": {
            "application/json": {
                "example": [
                    {
                        "property_id": "1",
                        "thumbnail": "https://www.example.com/image.jpg",
                        "address": "1234 Example St.",
                        "price": 100000,
                        "area": 100
                    }
                ]
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "Favorites not found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Favorites not found."
                }
            }
        }
    }
}

AddFavoriteResponseModelResponses: Dict[int, Dict[str, Any]] = {
    200: {
        "model": SuccessModel,
        "description": "Favorite added successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Favorite added successfully."
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
                    "detail": "Invalid input."
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Failed to add favorite.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Failed to add favorite."
                }
            }
        }
    }
}

DeleteFavoriteResponseModelResponses: Dict[int, Dict[str, Any]] = {
    200: {
        "model": SuccessModel,
        "description": "Favorite deleted successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Favorite deleted successfully."
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
                    "detail": "Invalid input."
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Failed to delete favorite.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Failed to delete favorite."
                }
            }
        }
    }
}

UpdateFavoriteResponseModelResponses: Dict[int, Dict[str, Any]] = {
    200: {
        "model": SuccessModel,
        "description": "Favorite updated successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Favorite updated successfully."
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
                    "detail": "Invalid input."
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Failed to update favorite.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Failed to update favorite."
                }
            }
        }
    }
}

# ReservationsBuyer

CreateReservationBuyerResponseModelResponses: Dict[int, Dict[str, Any]] = {
    201: {
        "model": SuccessModel,
        "description": "Reservation created successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Buyer reservation created successfully."
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

UpdateReservationsBuyerResponseModelResponses: Dict[int, Dict[str, Any]] = {
    200: {
        "model": ReservationsBuyer,
        "description": "Reservation updated successfully.",
        "content": {
            "application/json": {
                "example": {
                    "buyer_id": "615c44fdf641be001f0c1111",
                    "reservations": []
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
    400: {
        "model": ErrorModel,
        "description": "Invalid input data.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid input data."
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

DeleteReservationsBuyerResponseModelResponses: Dict[int, Dict[str, Any]] = {
    200: {
        "model": SuccessModel,
        "description": "Reservations deleted successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Buyer reservations deleted successfully."
                }
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "No reservations found or delete failed.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "No reservations found or delete failed."
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

GetReservationsBuyerResponseModelResponses: Dict[int, Dict[str, Any]] = {
    200: {
        "model": ReservationsBuyer,
        "description": "Reservations retrieved successfully.",
        "content": {
            "application/json": {
                "example": {
                    "buyer_id": "615c44fdf641be001f0c1111",
                    "reservations": []
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
                    "detail": "Failed to retrieve reservations."
                }
            }
        }
    }
}
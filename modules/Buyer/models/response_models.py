from pydantic import BaseModel
from typing import Dict, Any, List
from entities.MongoDB.Buyer.buyer import Buyer, FavouriteProperty
from entities.Redis.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB

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

# class CreateBuyerResponseModel(BaseModel):
#     detail: str
#     buyer_id: str

# CreateBuyerResponseModelResponses: Dict[int, Dict[str, Any]] = {
#     201: {
#         "model": SuccessModel,
#         "description": "Buyer created successfully.",
#         "content": {
#             "application/json": {
#                 "example": {
#                     "detail": "Buyer created successfully."
#                 }
#             }
#         }
#     },
#     400: {
#         "model": ErrorModel,
#         "description": "Invalid input or missing buyer info.",
#         "content": {
#             "application/json": {
#                 "example": {
#                     "detail": "Invalid buyer info."
#                 }
#             }
#         }
#     },
#     500: {
#         "model": ErrorModel,
#         "description": "Failed to create buyer.",
#         "content": {
#             "application/json": {
#                 "example": {
#                     "detail": "Failed to create buyer."
#                 }
#             }
#         }
#     }
# }

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

GetFavouritesResponseModelResponses: Dict[int, Dict[str, Any]] = {
    200: {
        "model": List[FavouriteProperty],
        "description": "Favourites retrieved successfully.",
        "content": {
            "application/json": {
                "example": [
                    {
                        "property_on_sale_id": "1",
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
        "description": "Favourites not found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Favourites not found."
                }
            }
        }
    }
}

AddFavouriteResponseModelResponses: Dict[int, Dict[str, Any]] = {
    200: {
        "model": SuccessModel,
        "description": "Favourite added successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Favourite added successfully."
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
        "description": "Failed to add favourite.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Failed to add favourite."
                }
            }
        }
    }
}

DeleteFavouriteResponseModelResponses: Dict[int, Dict[str, Any]] = {
    200: {
        "model": SuccessModel,
        "description": "Favourite deleted successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Favourite deleted successfully."
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
        "description": "Failed to delete favourite.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Failed to delete favourite."
                }
            }
        }
    }
}

# UpdateFavouriteResponseModelResponses: Dict[int, Dict[str, Any]] = {
#     200: {
#         "model": SuccessModel,
#         "description": "Favourite updated successfully.",
#         "content": {
#             "application/json": {
#                 "example": {
#                     "detail": "Favourite updated successfully."
#                 }
#             }
#         }
#     },
#     400: {
#         "model": ErrorModel,
#         "description": "Invalid input.",
#         "content": {
#             "application/json": {
#                 "example": {
#                     "detail": "Invalid input."
#                 }
#             }
#         }
#     },
#     500: {
#         "model": ErrorModel,
#         "description": "Failed to update favourite.",
#         "content": {
#             "application/json": {
#                 "example": {
#                     "detail": "Failed to update favourite."
#                 }
#             }
#         }
#     }
# }

# ReservationsBuyer

GetReservationsBuyerResponses = {
    200: {
        "model": List[ReservationB],
        "description": "Reservations retrieved successfully.",
        "content": {
            "application/json": {
                "example": [
                    {
                        "property_on_sale_id": "615c44fdf641be001f0c1111",
                        "date": "2021-09-01",
                        "time": "10:00-11:00 AM",
                        "thumbnail": "https://www.example.com/image",
                        "address": "1234 Example St."
                    }
                ]
            }
        }
    },
        
    404: {
        "model": ErrorModel,
        "description": "No reservations found for the buyer.",
        "content": {
            "application/json": {
                "example": {"detail": "No reservations found for buyer"}
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Internal server error occurred.",
        "content": {
            "application/json": {
                "example": {"detail": "Internal server error"}
            }
        }
    }
}

CreateReservationBuyerResponses: Dict[int, Dict[str, Any]] = {
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

UpdateReservationsBuyerResponses: Dict[int, Dict[str, Any]] = {
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

DeleteReservationsBuyerResponses: Dict[int, Dict[str, Any]] = {
    200: {
        "model": SuccessModel,
        "description": "Reservation deleted successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Buyer reservation deleted successfully."
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
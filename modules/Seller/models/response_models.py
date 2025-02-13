from pydantic import BaseModel
from entities.MongoDB.Seller.seller import Seller, SoldProperty, SellerPropertyOnSale
from entities.MongoDB.PropertyOnSale.property_on_sale import PropertyOnSale
from entities.Redis.ReservationsSeller.reservations_seller import ReservationsSeller
from typing import List, Dict, Any

class SuccessModel(BaseModel):
    detail: str

class ErrorModel(BaseModel):
    detail: str

# Seller

class SellerInfoResponseModel(BaseModel):
    seller_id: str
    agency_name: str
    email: str

GetSellerResponses = {
    200: {
        "model": SellerInfoResponseModel,
        "description": "Seller found.",
        "content": {
            "application/json": {
                "example": {
                    "seller_id": "507f1f77bcf86cd799439011",
                    "agency_name": "HomeXplore",
                    "email": "john@example.com",
                }
            }
        }
    },
    400: {
        "model": ErrorModel,
        "description": "Invalid seller id",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid seller id"
                }
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "Seller not found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Seller not found."
                }
            }
        }
    }
}

UpdateSellerResponses = {
    200: {
        "model": SuccessModel,
        "description": "Seller updated successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Seller updated successfully."
                }
            }
        }
    },
    400: {
        "model": ErrorModel,
        "description": "Invalid seller id or seller not found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid seller id"
                }
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "Seller not found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Seller not found."
                }
            }
        }
    }
}

DeleteSellerResponses = {
    200: {
        "model": SuccessModel,
        "description": "Seller deleted successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Seller deleted successfully."
                }
            }
        }
    },
    400: {
        "model": ErrorModel,
        "description": "Invalid seller id",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid seller id"
                }
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "Seller not found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Seller not found."
                }
            }
        }
    }
}

#CONSISTENT
GetSoldPropertiesResponses = {
    200: {
        "model": List[SoldProperty],
        "description": "Sold properties retrieved successfully.",
        "content": {
            "application/json": {
                "example": {
                    "seller_id": "507f1f77bcf86cd799439011",
                    "agency_name": "HomeXplore",
                    "email": "john@example.com",
                    "phone_number": "123-456-7890",
                    "properties_on_sale": [],
                    "sold_properties": [
                        {
                            "sold_property_id": "507f1f77bcf86cd799439012",
                            "city": "New York",
                            "neighbourhood": "Manhattan",
                            "price": 1000000,
                            "thumbnail": "https://example.com/image.jpg",
                            "type": "Apartment",
                            "area": 100,
                            "registration_date": "2021-01-01T00:00:00",
                            "sell_date": "2021-06-01T00:00:00"
                        }
                    ]
                }
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "Input error or data error.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Seller not found."
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Internal error.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Failed to retrieve sold properties."
                }
            }
        }
    }
}

#CONSISTENT
GetPropertiesOnSaleResponses = {
    200: {
        "model": List[PropertyOnSale],
        "description": "Properties on sale retrieved successfully.",
        "content": {
            "application/json": {
                "example": [
                    {
                        "property_on_sale_id": "60d5ec49f8d2e30b8c8b4567",
                        "city": "New York",
                        "neighbourhood": "Brooklyn",
                        "address": "1234 Brooklyn St.",
                        "price": 500000,
                        "thumbnail": "https://www.example.com/thumbnail.jpg",
                        "disponibility": {
                            "day": "Monday",
                            "time": "10:00-11:00 AM",
                            "max_attendees": 5
                        }
                    }
                ]
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "Input error or data error.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Seller not found."
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Internal error.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Failed to retrieve properties on sale."
                }
            }
        }
    }
}



# SellerReservations

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
                    "reservations": []
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


class OpenHouseOccurrence(BaseModel):
    city: str
    address: str
    time: str
    

GetOpenHouseEventsResponses = {
    200: {
        "model": List[OpenHouseOccurrence],
        "description": "Open house events retrieved successfully.",
        "content": {
            "application/json": {
                "example": [
                    {
                        "city": "New York",
                        "address": "1234 Brooklyn St.",
                        "time": "10:00-11:00 AM"
                    }
                ]
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "No open house events found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "No open house events found."
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Failed to fetch open house events.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Failed to fetch open house events."
                }
            }
        }
    }
}



# PropertyOnSale

class CreatePropertyOnSaleResponseModel(BaseModel):
    detail: str
    property_on_sale_id: str

CreatePropertyOnSaleResponses = {
    201: {
        "model": CreatePropertyOnSaleResponseModel,
        "description": "Property created successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Property created successfully.",
                    "property_on_sale_id": "60d5ec49f8d2e30b8c8b4567"
                }
            }
        }
    },
    400: {
        "model": ErrorModel,
        "description": "Invalid property information.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid property information."
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Failed to create property.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Failed to create property."
                }
            }
        }
    }
}

DeletePropertyOnSaleResponses = {
    200: {
        "model": SuccessModel,
        "description": "Property deleted successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Property deleted successfully."
                }
            }
        }
    },
    400: {
        "model": ErrorModel,
        "description": "Invalid property id.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid property id."
                }
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "Property not found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Property not found."
                }
            }
        }
    }
}

UpdatePropertyOnSaleResponses = {
    200: {
        "model": SuccessModel,
        "description": "Property updated successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Property updated successfully."
                }
            }
        }
    },
    400: {
        "model": ErrorModel,
        "description": "Invalid property id.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid property id."
                }
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "Property not found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Property not found."
                }
            }
        }
    }
}

SellPropertyOnSaleResponses = {
    200: {
        "model": SuccessModel,
        "description": "Property sold successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Property sold successfully."
                }
            }
        }
    },
    400: {
        "model": ErrorModel,
        "description": "Invalid property id.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid property id."
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Failed to sell property.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Failed to sell property."
                }
            }
        }       
    }
}

GetFilteredPropertiesOnSaleResponses = {
    200: {
        "model": List[PropertyOnSale],
        "description": "Filtered properties retrieved successfully.",
        "content": {
            "application/json": {
                "example": [
                    {
                        "property_on_sale_id": "60d5ec49f8d2e30b8c8b4567",
                        "city": "New York",
                        "neighbourhood": "Brooklyn",
                        "address": "1234 Brooklyn St.",
                        "price": 500000,
                        "thumbnail": "https://www.example.com/thumbnail.jpg",
                        "type": "House",
                        "area": 2000,
                        "registration_date": "2021-06-25T12:00:00",
                        "bed_number": 3,
                        "bath_number": 2,
                        "description": "Beautiful house in Brooklyn.",
                        "photos": ["https://www.example.com/photo1.jpg"],
                        "disponibility": {
                            "day": "Monday",
                            "time": "10:00-11:00 AM",
                            "max_attendees": 5
                        }
                    }
                ]
            }
        }
    },
    400: {
        "model": ErrorModel,
        "description": "Invalid search parameters.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid search parameters."
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

#Analytics

class GroupedRevenuesPerNeighbourhood(BaseModel):
    houses_sold: int
    revenue: int
    neighbourhood: str
class Analytics2ResponseModel(BaseModel):
    detail: str
    result: List[GroupedRevenuesPerNeighbourhood]

Analytics2Responses = {
    200: {
        "model": Analytics2ResponseModel,
        "description": "Analytics data retrieved successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Aggregated data finished successfully",
                    "result": [
                        {
                            "neighbourhood": "Brooklyn",
                            "house_sold": 10,
                            "revenue": 5000000
                        },
                        {
                            "neighbourhood": "Manhattan",
                            "house_sold": 5,
                            "revenue": 3000000
                        }
                    ]
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
                    "detail": "Start date must be before end date."
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Database client not found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Database client not found"
                }
            }
        }
    }
}


class GroupedTimeToSell(BaseModel):
    avg_time_to_sell: int
    num_house: int
    neighbourhood: str
    
class Analytics3ResponseModel(BaseModel):
    detail: str
    result: List[GroupedTimeToSell]
    
 
Analytics3Responses = {
    200: {
        "model": Analytics3ResponseModel,
        "description": "Analytics data retrieved successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Aggregated data finished successfully",
                    "result": [
                        {
                            "neighbourhood": "Brooklyn",
                            "house_sold": 10,
                            "revenue": 5000000
                        },
                        {
                            "neighbourhood": "Manhattan",
                            "house_sold": 5,
                            "revenue": 3000000
                        }
                    ]
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Database client not found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Database client not found"
                }
            }
        }
    }
}
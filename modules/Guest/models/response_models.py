from pydantic import BaseModel
from entities.MongoDB.PropertyOnSale.property_on_sale import PropertyOnSale
from typing import List, Dict, Any

class SuccessModel(BaseModel):
    detail: str

class ErrorModel(BaseModel):
    detail: str


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

GetRandomPropertiesOnSaleResponses = {
    200: {
        "model": List[PropertyOnSale],
        "description": "Random properties retrieved successfully.",
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


GetPropertyOnSaleResponses = {
    200: {
        "model": PropertyOnSale,
        "description": "Property found.",
        "content": {
            "application/json": {
                "example": {
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
                    "photos": ["https://www.example.com/photo1.jpg", "https://www.example.com/photo2.jpg"],
                    "disponibility": {
                        "day": "Monday",
                        "time": "10:00-11:00 AM",
                        "max_attendees": 5
                    }
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


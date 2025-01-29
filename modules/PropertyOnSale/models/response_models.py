from pydantic import BaseModel
from entities.PropertyOnSale.property_on_sale import PropertyOnSale


class SuccessModel(BaseModel):
    detail: str

class ErrorModel(BaseModel):
    detail: str
    
class CreatePropertyOnSaleResponseModel(BaseModel):
    detail: str
    property_id: str
    
    
CreatePropertyOnSaleResponses = {
    201: {
        "model": CreatePropertyOnSaleResponseModel,
        "description": "Property created successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Property created successfully.",
                    "property_id": "60d5ec49f8d2e30b8c8b4567"
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


GetPropertiesOnSaleResponses = {
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
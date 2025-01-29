from pydantic import BaseModel
from entities.Seller.seller import Seller

class SuccessModel(BaseModel):
    detail: str

class ErrorModel(BaseModel):
    detail: str

class CreateSellerResponseModel(BaseModel):
    detail: str
    seller_id: str

CreateSellerResponses = {
    201: {
        "model": CreateSellerResponseModel,
        "description": "Seller created successfully.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Seller created successfully.",
                    "seller_id": "507f1f77bcf86cd799439011"
                }
            }
        }
    },
    400: {
        "model": ErrorModel,
        "description": "Invalid seller information.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid seller information."
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "Failed to create seller.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Failed to create seller."
                }
            }
        }
    }
}

GetSellerResponses = {
    200: {
        "model": dict,
        "description": "Seller found.",
        "content": {
            "application/json": {
                "example": {
                    "seller_id": "507f1f77bcf86cd799439011",
                    "agency_name": "HomeXplore",
                    "email": "john@example.com",
                    "phone_number": "123-456-7890",
                    "property_on_sale": [],
                    "sold_property": []
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

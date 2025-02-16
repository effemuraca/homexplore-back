from pydantic import BaseModel
from entities.MongoDB.PropertyOnSale.property_on_sale import PropertyOnSale
from entities.Neo4J.City.city import City
from entities.Neo4J.Neighbourhood.neighbourhood import Neighbourhood
from entities.Neo4J.POI.poi import POI
from entities.Neo4J.PropertyOnSaleNeo4J.property_on_sale_neo4j import PropertyOnSaleNeo4J
from typing import List, Dict, Any
from typing import Optional
from modules.Guest.models.guest_models import SummaryPropertyOnSale

class SuccessModel(BaseModel):
    detail: str

class ErrorModel(BaseModel):
    detail: str




GetFilteredPropertiesOnSaleResponses = {
    200: {
        "model": List[SummaryPropertyOnSale],
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
                    }
                ]
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "No properties found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "No properties found."
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
        "model": List[SummaryPropertyOnSale],
        "description": "Random properties retrieved successfully.",
        "content": {
            "application/json": {
                "example": [
                    {
                        "property_on_sale_id": "60d5ec49f8d2e30b8c8b4567",
                        "address": "1234 Brooklyn St.",
                        "price": 500000,
                        "thumbnail": "https://www.example.com/thumbnail.jpg",
                    }
                ]
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "No properties found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "No properties found."
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
                        "time": "10:00 AM - 11:00 AM",
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


# Map
class CityAndNeighbourhood(BaseModel):
    city: City
    neighbourhood: Neighbourhood

GetCityAndNeighbourhoodResponses = {
    200: {
        "model": CityAndNeighbourhood,
        "description": "City and neighbourhood found.",
        "content": {
            "application/json": {
                "example": {
                    "city": {
                        "name": "New York",
                        "coordinates": {
                            "latitude": 40.7128,
                            "longitude": -74.0060
                        },
                        "safety_index": 70.5,
                        "health_care_index": 75.3,
                        "cost_of_living_index": 80.2,
                        "pollution_index": 60.8
                    },
                    "neighbourhood": {
                        "name": "Brooklyn",
                        "coordinates": {
                            "latitude": 40.6782,
                            "longitude": -73.9442
                        }
                    }
                }
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "City or neighbourhood not found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "City or neighbourhood not found."
                }
            }
        }
    }
}

GetPOIsResponses = {
    200: {
        "model": List[POI],
        "description": "POIs found.",
        "content": {
            "application/json": {
                "example": [
                    {
                        "name": "School Yankees",
                        "type": "school",
                        "coordinates": {
                            "latitude": 40.7128,
                            "longitude": -74.0060
                        }
                    },
                    {
                        "name": "Hospital Amber",
                        "type": "hospital",
                        "coordinates": {
                            "latitude": 40.7128,
                            "longitude": -74.0060
                        },
                    }
                ]
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

            

GetNearPropertiesResponses = {
    200: {
        "model": List[PropertyOnSaleNeo4J],
        "description": "Near properties found.",
        "content": {
            "application/json": {
                "example": [
                    {
                        "property_on_sale_id": "60d5ec49f8d2e30b8c8b4567",
                        "coordinates": {
                            "latitude": 40.7128,
                            "longitude": -74.0060
                        },
                        "price": 500000,
                        "type": "House",
                        "thumbnail": "https://www.example.com/thumbnail.jpg",
                        "score": 67.89,
                    },
                    {
                        "property_on_sale_id": "60d5ec49f8d2e30b8c8b4568",
                        "coordinates": {
                            "latitude": 40.7128,
                            "longitude": -74.0060
                        },
                        "price": 600000,
                        "type": "Apartment",
                        "thumbnail": "https://www.example.com/thumbnail.jpg",
                        "score": 70.12,
                    }
                ]
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
# author: @VinStan1
# purpose:
#     this file contains all the response models for the Auth module, for documentation purposes.

from pydantic import BaseModel

class ErrorModel(BaseModel):
    detail: str

class UserLoginResponseModel(BaseModel):
    access_token: str
    refresh_token: str

UserLoginResponseModelResponses = {
    200: {
        "model": UserLoginResponseModel,
        "description": "Successful login, returns access and refresh tokens.",
        "content": {
            "application/json": {
                "example": {
                    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOi...",
                    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOi..."
                }
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "No user found with the provided email.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "User not found"
                }
            }
        }
    },
    401: {
        "model": ErrorModel,
        "description": "Incorrect password or user not verified.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Wrong credentials"
                }
            }
        }
    }
}


class RefreshAccessTokenResponseModel(BaseModel):
    access_token: str

RefreshAccessTokenResponseModelResponses = {
    200: {
        "model": RefreshAccessTokenResponseModel,
        "description": "Successful refresh, returns new access token.",
        "content": {
            "application/json": {
                "example": {
                    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOi..."
                }
            }
        }
    },
    401: {
        "model": ErrorModel,
        "description": "Invalid refresh token.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid refresh token"
                }
            }
        }
    }
}

class GetMeResponseModel(BaseModel):
    id: int
    user_type_id: int
    first_name: str
    last_name: str
    email: str
    created_at: str
    updated_at: str

GetMeResponseModelResponses = {
    200: {
        "model": GetMeResponseModel,
        "description": "Successful retrieval of user data.",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "user_type_id": 0,
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "johndoe@test.com",
                    "created_at": "2021-01-01T00:00:00",
                    "updated_at": "2021-01-01T00:00:00"
                }
            }
        }
    },
    401: {
        "model": ErrorModel,
        "description": "User not verified.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "User not verified"
                }
            }
        }
    }
}


class UserRegisterResponseModel(BaseModel):
    message: str

UserRegisterResponseModelResponses = {
    201: {
        "model": UserRegisterResponseModel,
        "description": "Successful registration.",
        "content": {
            "application/json": {
                "example": {
                    "message": "User created"
                }
            }
        }
    },
    409: {
        "model": ErrorModel,
        "description": "Email already exists.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Email already exists"
                }
            }
        }
    },
    400: {
        "model": ErrorModel,
        "description": "Error.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Error"
                }
            }
        }
    },
    500: {
        "model": ErrorModel,
        "description": "User not created.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "User not created"
                }
            }
        }
    }
}

class GetUserResponseModel(BaseModel):
    id: int
    user_type_id: int
    first_name: str
    last_name: str
    email: str
    created_at: str
    updated_at: str
    verified: bool

GetUserResponseModelResponses = {
    200: {
        "model": GetUserResponseModel,
        "description": "Successful retrieval of user.",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "user_type_id": 0,
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "johndoe@test.com",
                    "created_at": "2021-01-01T00:00:00",
                    "updated_at": "2021-01-01T00:00:00",
                    "verified": True,
                }
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "User not found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "User not found"
                }
            }
        }
    },
    403: {
        "model": ErrorModel,
        "description": "User is not admin.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "User is not admin"
                }
            }
        }
    }
}

class UserDeleteResponseModel(BaseModel):
    message: str
    
UserDeleteResponseModelResponses = {
    200: {
        "model": UserDeleteResponseModel,
        "description": "Successful deletion of user.",
        "content": {
            "application/json": {
                "example": {
                    "message": "User deleted"
                }
            }
        }
    },
    404: {
        "model": ErrorModel,
        "description": "User not found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "User not found"
                }
            }
        }
    },
    403: {
        "model": ErrorModel,
        "description": "User is not admin.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "User is not admin"
                }
            }
        }
    }
}
        



class GetUsersResponseModel(BaseModel):
    users: list[GetUserResponseModel]
    
GetUsersResponseModelResponses = {
    200: {
        "model": GetUsersResponseModel,
        "description": "Successful retrieval of users.",
        "content": {
            "application/json": {
                "example": {
                    "users": [
                        {
                            "id": 1,
                            "user_type_id": 0,
                            "first_name": "John",
                            "last_name": "Doe",
                            "email": "johndoe@test.com",
                            "created_at": "2021-01-01T00:00:00",
                            "updated_at": "2021-01-01T00:00:00",
                            "verified": True,
                        },
                        {
                            "id": 2,
                            "user_type_id": 0,
                            "first_name": "Jane",
                            "last_name": "Doe",
                            "email": "janedoe@test.com",
                            "created_at": "2021-01-01T00:00:00",
                            "updated_at": "2021-01-01T00:00:00",
                            "verified": True,
                        }
                    ]
                }
            }
        }
    },
    403: {
        "model": ErrorModel,
        "description": "User is not admin.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "User is not admin"
                }
            }
        }
    }
}
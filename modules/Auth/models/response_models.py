from pydantic import BaseModel

class SuccessModel(BaseModel):
    detail: str

class ErrorModel(BaseModel):
    detail: str

class LoginResponseModel(BaseModel):
    access_token: str
    refresh_token: str

LoginResponseModelResponses = {
    200: {
        "model": LoginResponseModel,
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

class RegisterResponseModel(BaseModel):
    message: str

RegisterResponseModelResponses = {
    201: {
        "model": RegisterResponseModel,
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
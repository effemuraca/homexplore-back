from pydantic import BaseModel, EmailStr, Field

from entities.User import models_user as UserModels


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=32, example="ThisIsAPassword123!")

class UserCreateModel(UserModels.UserCreateModel):
    password: str = Field(..., min_length=8, max_length=32, example="ThisIsAPassword123!")
    
class UserReadModel(UserModels.UserBaseModel):
    id: int

class UserUpdateModel(UserCreateModel):
    id: int
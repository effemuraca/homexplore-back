# purpose:
#     this file provides helper functions that are based on the auth module, such as getters and role checks.
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from fastapi import Depends, HTTPException, Request, status
from typing import Union
from bcrypt import hashpw, gensalt, checkpw
from .JwtHandler import JWTHandler

def get_user_by_access_token(access_token: str) -> Union[User, None]:
    """
    Get the user from the access token.
    
    Args:
        access_token (str): The access token to get the user from.
    
    Returns:
        Union[User, None]: The user if the access token is valid, None otherwise.
    """
    user_id = JWTHandler.verifyAccessToken(access_token)
    user = get_user_by_id(int(user_id))
    if(user):
        return user
    else:
        return None
            
def hash_password(password: str) -> str:
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

def verify_hashed_password(hashed: str, password: str) -> bool:
    return checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
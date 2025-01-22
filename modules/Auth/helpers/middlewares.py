# author: @VinStan1
# purpose:
#     this file contains the middleware function is_authenticated, useful to the other modules, and will contain
#     other middleware functions with a role-based access control in the future.

from fastapi import Header, HTTPException
from .JwtHandler import JWTHandler
from typing import Optional
from entities.User.methods_user import get_user_by_id

def is_authenticated(authorization: Optional[str] = Header(None)) -> bool:
    """
    Check if the user is authenticated.

    Args:
        authorization (Optional[str], optional): The authorization header. Defaults to Header(None).

    Returns:
        bool: True if the user is authenticated, raises an HTTPException otherwise.
    """
    if authorization is None:
        raise HTTPException(
            status_code=401,
            detail="No access token provided"
        )
    user_id = JWTHandler.verifyAccessToken(authorization)
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid access token"
        )
    return True

def is_admin(authorization: Optional[str] = Header(None)) -> bool:
    """
    Check if the user is an admin.

    Args:
        authorization (Optional[str], optional): The authorization header. Defaults to Header(None).

    Returns:
        bool: True if the user is an admin, raises an HTTPException otherwise.
    """
    if not is_authenticated(authorization):
        raise HTTPException(
            status_code=401,
            detail="User is not authenticated"
        )
    user_id = JWTHandler.verifyAccessToken(authorization)
    user = get_user_by_id(user_id)
    if user.user_type_id != 10:
        raise HTTPException(
            status_code=403,
            detail="User is not an admin"
        )
    return True
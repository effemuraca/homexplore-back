from fastapi import Header, HTTPException
from .JwtHandler import JWTHandler
from typing import Optional

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
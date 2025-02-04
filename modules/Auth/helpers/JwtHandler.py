from os import getenv
from datetime import timedelta, datetime
from jose import JWTError, jwt
from typing import Union, Any
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from os import environ
from config.config import settings

class JWTHandler(HTTPBearer):
    """This class is a helper class for the creation and verification of JWT tokens.
       It supports multiple user types with separate secret keys.
    """

    secret_seller = environ.get('JWT_SECRET_KEY_SELLER', settings.jwt_secret_key_seller)
    secret_buyer = environ.get('JWT_SECRET_KEY_BUYER', settings.jwt_secret_key_buyer)
    algo = environ.get('JWT_ALGORITHM', settings.jwt_algorithm)
    expireMins = int(environ.get('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', settings.jwt_access_token_expire_minutes))

    @staticmethod
    def get_secret_by_user_type(user_type: str) -> str:
        """Returns the appropriate secret key based on the user type."""
        if user_type == "seller":
            return JWTHandler.secret_seller
        elif user_type == "buyer":
            return JWTHandler.secret_buyer
        else:
            raise ValueError("Invalid user type")

    @staticmethod
    def createAccessToken(subject: Union[str, Any], user_type: str, expires_delta: Union[int, None] = None, tokenType: str = "access") -> str:
        """
        Creates a JWT token with the given subject, user type, and expiration time.
        """
        if expires_delta is not None:
            expires = datetime.utcnow() + timedelta(minutes=expires_delta)
        else:
            expires = datetime.utcnow() + timedelta(minutes=JWTHandler.expireMins)
        
        secret = JWTHandler.get_secret_by_user_type(user_type)
        to_encode = {"exp": expires, "sub": str(subject), "type": tokenType, "user_type": user_type}
        encoded_jwt = jwt.encode(to_encode, secret, algorithm=JWTHandler.algo)
        return encoded_jwt

    @staticmethod
    def createRefreshToken(subject: Union[str, Any], user_type: str, expires_delta: Union[int, None] = None) -> str:
        return JWTHandler.createAccessToken(subject, user_type, expires_delta, "refresh")

    @staticmethod
    def verifyAccessToken(token: str) -> Union[tuple[str, str], None]:
        """
        Verifies the given token and returns its subject and user type if the token is valid, otherwise None.
        """
        try:
            # Use get_unverified_claims to extract the payload without verifying the signature.
            unverified_payload = jwt.get_unverified_claims(token)
            user_type = unverified_payload.get("user_type")
            secret = JWTHandler.get_secret_by_user_type(user_type)

            # Now decode and verify the token using the correct secret and algorithm.
            payload = jwt.decode(token, secret, algorithms=[JWTHandler.algo])

            if datetime.fromtimestamp(payload["exp"]) < datetime.utcnow() or payload["type"] != "access":
                return None
            return payload["sub"], payload["user_type"]
        except (JWTError, ValueError) as e:
            return None

    @staticmethod
    def verifyRefreshToken(token: str) -> Union[str, None]:
        try:
            unverified_payload = jwt.get_unverified_claims(token)
            user_type = unverified_payload.get("user_type")
            secret = JWTHandler.get_secret_by_user_type(user_type)

            payload = jwt.decode(token, secret, algorithms=[JWTHandler.algo])
            
            if datetime.fromtimestamp(payload["exp"]) < datetime.utcnow() or payload["type"] != "refresh":
                return None
            return payload["sub"], payload["user_type"]
        except (JWTError, ValueError):
            return None

    def __init__(self, auto_error: bool = True):
        super(JWTHandler, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Union[str, None]:
        """
        Verifies the token in the Authorization header of the request and returns the token if it is valid.
        
        Raises:
            HTTPException: 401 - Invalid token, expired token, or incorrect authentication scheme.
        """
        try:
            credentials: Union[HTTPAuthorizationCredentials, None] = await super(JWTHandler, self).__call__(request)

            if credentials is None:
                raise HTTPException(status_code=401, detail="Authorization header missing or invalid.")

            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=401, detail="Invalid authentication scheme. Expected 'Bearer'.")

            access_token_data = JWTHandler.verifyAccessToken(credentials.credentials)
            if access_token_data:
                return credentials.credentials

            refresh_token_data = JWTHandler.verifyRefreshToken(credentials.credentials)
            if refresh_token_data:
                return credentials.credentials 

            raise HTTPException(status_code=401, detail="Invalid token or expired token.")

        except HTTPException as e:
            raise HTTPException(status_code=401, detail=e.detail)

        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid authorization code.") from e

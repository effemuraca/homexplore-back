# purpose:
#     this file contains the JWTHandler class, which is a helper class for the creation and verification of JWT tokens.

from os import getenv
from datetime import timedelta
from datetime import datetime
from jose import JWTError, jwt
from typing import Union, Any
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from os import environ
from config.config import settings

class JWTHandler(HTTPBearer):
    """This class is a helper class for the creation and verification of JWT tokens.
    For the creation of the tokens, the class uses the jose library, which allows 
    a simple and secure way to create and verify tokens.
    The type of token is "Bearer" and the token is created with the HS256 algorithm.

    To use this class, 3 environment variables are required:
    - JWT_SECRET_KEY
    - JWT_ALGORITHM
    - JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    """

    secret = environ.get('JWT_SECRET_KEY')
    algo = environ.get('JWT_ALGORITHM')
    expireMins = environ.get('JWT_ACCESS_TOKEN_EXPIRE_MINUTES')
    
    if secret is None or secret == '':
        secret = settings.jwt_secret_key
    if algo is None or algo == '':
        algo = settings.jwt_algorithm
    if expireMins is None or expireMins == '':
        expireMins = settings.jwt_access_token_expire_minutes

    @staticmethod
    def createAccessToken(subject: Union[str, Any], expires_delta: Union[int, None] = None, tokenType: str = "access") -> str:
        """
        Creates a JWT token with the given subject and expiration time.
        """
        if expires_delta is not None:
            expires = datetime.utcnow() + timedelta(minutes=expires_delta)
        else:
            expires = datetime.utcnow() + timedelta(minutes=int(JWTHandler.expireMins)) # type: ignore        
        
        to_encode = {"exp": expires, "sub": str(subject), "type": tokenType}
        encoded_jwt = jwt.encode(to_encode, JWTHandler.secret, JWTHandler.algo) # type: ignore        
        return encoded_jwt

    @staticmethod
    def createRefreshToken(subject: Union[str, Any], expires_delta: Union[int, None] = None) -> str:
        return JWTHandler.createAccessToken(subject, expires_delta, "refresh")

    @staticmethod
    def verifyAccessToken(token: str) -> Union[str, None]:
        """
        Verifies the given token and returns its subject if the token is valid, otherwise None.
        """
        try:
            payload = jwt.decode(token, JWTHandler.secret, JWTHandler.algo) # type: ignore   
            # check if token is expired
            if datetime.fromtimestamp(payload["exp"]) < datetime.utcnow() or payload["type"] != "access":
                return None         
            return payload["sub"]
        except JWTError:
            return None

    @staticmethod
    def verifyRefreshToken(token: str) -> Union[str, None]:
        try:
            payload = jwt.decode(token, JWTHandler.secret, JWTHandler.algo) # type: ignore   
            # check if token is expired
            if datetime.fromtimestamp(payload["exp"]) < datetime.utcnow() or payload["type"] != "refresh":
                return None         
            return payload["sub"]
        except JWTError:
            return None

    def __init__(self, auto_error: bool = True):
        super(JWTHandler, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Union[str, None]:
        """This method is called when the class is used as a dependency in a FastAPI route. 
        It verifies the token in the Authorization header of the request and returns the token if it is valid.
        
        Example usage:
        ```
        @app.get("/me")
        async def get_me(access_token: str = Depends( JWTHandler() )):
            user_id = JWTHandler.verifyAccessToken(access_token)
            user = get_user_by_id(user_id)
            return user
        ```

        Args:
            request (Request): The request object from the FastAPI route.

        Raises:
            HTTPException: 401 - Invalid authentication scheme.
            HTTPException: 401 - Invalid token or expired token.
            HTTPException: 401 - Invalid authorization code.

        Returns:
            Union[str, None]: The token if it is valid.
        """
        try:
            credentials: Union[HTTPAuthorizationCredentials, None] = await super(JWTHandler, self).__call__(request)
            if credentials:
                if not credentials.scheme == "Bearer":
                    raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
                if not JWTHandler.verifyAccessToken(credentials.credentials) and not JWTHandler.verifyRefreshToken(credentials.credentials):
                    raise HTTPException(status_code=401, detail="Invalid token or expired token.")
                return credentials.credentials
            else:
                raise HTTPException(status_code=401, detail="Invalid authorization code.")
        except HTTPException as e:
            if e.status_code in [400, 401, 402, 403]:
                raise HTTPException(status_code=401, detail=e.detail)
            raise e
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid authorization code.") from e
    
        

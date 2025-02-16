from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse

from modules.Auth.helpers.JwtHandler import JWTHandler
from modules.Auth.helpers.auth_helpers import hash_password, verify_hashed_password
from entities.MongoDB.Buyer.db_buyer import BuyerDB
from entities.MongoDB.Seller.db_seller import SellerDB
from entities.MongoDB.Buyer.buyer import Buyer
from entities.MongoDB.Seller.seller import Seller
from modules.Auth.models import response_models as ResponseModels
from modules.Auth.models import auth_models as AuthModels

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/login", response_model=ResponseModels.LoginResponseModel, responses= ResponseModels.LoginResponseModelResponses)
def login(login_info: AuthModels.Login, user_type: str):
    """
    Log in a user and return the access and refresh tokens, access token can be used on the padlock to unlock reserved features.

    Args:
        user_type (str): The type of user logging in ("buyer" or "seller").
    
    Body: (AuthModels.Login): The login credentials.

    Raises:
        HTTPException: 400 if the user type is invalid or the email is missing.
                       404 if the user is not found.
                       401 if the password is incorrect.

    Returns:
        JSONResponse: The access and refresh tokens.
    """
    if user_type not in ["buyer", "seller"]:
        raise HTTPException(status_code=400, detail="Invalid user type")
    
    if user_type == "buyer":
        user_db = BuyerDB()
        result = user_db.get_buyer_by_email(login_info.email)
    elif user_type == "seller":
        user_db = SellerDB()
        result = user_db.get_seller_by_email(login_info.email)
    
    if result == 404:
        raise HTTPException(status_code=404, detail="User not found")
    elif result == 400:
        raise HTTPException(status_code=400, detail="email not given")
    
    user = getattr(user_db, user_type)
    user_id = getattr(user, f"{user_type}_id")
    
    pw_is_correct = verify_hashed_password(user.password, login_info.password)
    if not pw_is_correct:
        raise HTTPException(status_code=401, detail="Wrong credentials")
    
    acc_token = JWTHandler.createAccessToken(user_id, user_type, 60*24*7)
    ref_token = JWTHandler.createRefreshToken(user_id, user_type, 60*24*7)
    return JSONResponse(
        content= {
            "access_token": acc_token,
            "refresh_token": ref_token
        },
        status_code=200
    )
    
@auth_router.post("/jwt/refresh", response_model=ResponseModels.RefreshAccessTokenResponseModel, responses= ResponseModels.RefreshAccessTokenResponseModelResponses)
def refreshAccToken(refresh_token: str = Depends(JWTHandler())):
    """
    Refresh the access token using a refresh token.

    Raises:
        HTTPException: 401 if the refresh token is invalid.

    Returns:
        JSONResponse: The new access token.
    """
    user_id, user_type = JWTHandler.verifyRefreshToken(refresh_token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="invalid refresh token")
    acc_token = JWTHandler.createAccessToken(user_id, user_type, 60*24*7)
    return JSONResponse(
        content= {
            "access_token": acc_token,
        },
        status_code=200
    )

@auth_router.post("/signup/buyer", response_model=ResponseModels.SuccessModel, responses=ResponseModels.RegisterResponseModelResponses)
def register_buyer(user_info: AuthModels.CreateBuyer):
    """
    Register a buyer.

    Body:
        (AuthModels.CreateBuyer): The buyer information.

    Raises:
        HTTPException: 409 if the email already exists.
                       500 if there is an error during buyer creation.
                       400 if the provided data is invalid.

    Returns:
        JSONResponse: A success message if registration is successful.
    """
    # Check if the email already exists in the buyer database
    buyer_db = BuyerDB()
    existing_check = buyer_db.get_buyer_by_email(user_info.email)
    if existing_check != 404:
        raise HTTPException(status_code=409, detail="Email already exists")

    # Hash of the password and creation of the user
    hashed_pw = hash_password(user_info.password)
    user_info.password = hashed_pw
    buyer_db.buyer = Buyer(**user_info.model_dump())
    result = buyer_db.create_buyer()
    if result == 500:
        raise HTTPException(status_code=500, detail="Error during buyer creation")
    elif result == 400:
        raise HTTPException(status_code=400, detail="Error in the information provided")

    return JSONResponse(
        content={
            "detail": "Buyer created successfully"
        },
        status_code=201
    )


@auth_router.post("/signup/seller", response_model=ResponseModels.SuccessModel, responses=ResponseModels.RegisterResponseModelResponses)
def register_seller(user_info: AuthModels.CreateSeller):
    """
    Register a seller.

    Body:
       (AuthModels.CreateSeller): The seller information.

    Raises:
        HTTPException: 409 if the email already exists.
                       500 if there is an error during seller creation.
                       400 if the provided data is invalid.

    Returns:
        JSONResponse: A success message if registration is successful.
    """
    # Check if the email already exists in the seller database
    seller_db = SellerDB()
    existing_check = seller_db.get_seller_by_email(user_info.email)
    if existing_check != 404:
        raise HTTPException(status_code=409, detail="Email already exists")

    # Hash of the password and creation of the user
    hashed_pw = hash_password(user_info.password)
    user_info.password = hashed_pw
    seller_db.seller = Seller(**user_info.model_dump())
    result = seller_db.create_seller()
    if result == 500:
        raise HTTPException(status_code=500, detail="Error during seller creation")
    elif result == 400:
        raise HTTPException(status_code=400, detail="Error in the information provided")

    return JSONResponse(
        content={
            "detail": "Seller created successfully"
        },
        status_code=201
    )
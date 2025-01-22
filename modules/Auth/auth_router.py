from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse

from modules.Auth.helpers.auth_helpers import JWTHandler, hash_password, verify_hashed_password
from entities.User.methods_user import create_user, get_user_by_email, get_user_by_id, update_user_by_id, is_admin_check, delete_user_by_id
from entities.Candidate.methods_candidate import create_candidate, delete_candidate
from modules.Auth.models import response_models as ResponseModels
from modules.Auth.models import auth_models as UserModels

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/login", response_model=ResponseModels.UserLoginResponseModel, responses= ResponseModels.UserLoginResponseModelResponses)
def login_handler(loginInfo: UserModels.UserLoginModel):
    return login(loginInfo)

@auth_router.get("/me", response_model=ResponseModels.GetMeResponseModel, responses= ResponseModels.GetMeResponseModelResponses)
def me_handler(access_token: str = Depends(JWTHandler())):
    return me(access_token)

@auth_router.post("/jwt/refresh", response_model=ResponseModels.RefreshAccessTokenResponseModel, responses= ResponseModels.RefreshAccessTokenResponseModelResponses)
def refreshAccToken_handler(refresh_token: str = Depends(JWTHandler())):
    return refreshAccToken(refresh_token)

@auth_router.post("/register", response_model=ResponseModels.UserRegisterResponseModel, responses= ResponseModels.UserRegisterResponseModelResponses)
async def register_handler(userInfo: UserModels.UserCreateModel):
    return await register(userInfo)
    
@auth_router.get("/user", response_model=ResponseModels.GetUserResponseModel, responses= ResponseModels.GetUserResponseModelResponses)
def getUser_handler(user_id: int, access_token: str = Depends (JWTHandler())):
    return getUser(user_id, access_token)

@auth_router.delete("/delete-user")
def delete_user_handler(user_id: int, access_token: str = Depends(JWTHandler())):
    return delete_user(user_id, access_token)

    
def login(loginInfo: UserModels.UserLoginModel):
    user = get_user_by_email(loginInfo.email)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    if not user.verified:
        raise HTTPException(status_code=401, detail="user not verified")
    pw_is_correct = verify_hashed_password(user.password, loginInfo.password)
    if not pw_is_correct:
        raise HTTPException(status_code=401, detail="Wrong credentials")
    user_is_verified = user.verified
    if not user_is_verified:
        raise HTTPException(status_code=401, detail="user not verified")
    acc_token = JWTHandler.createAccessToken(user.id, 60*24*7)
    ref_token = JWTHandler.createRefreshToken(user.id, 60*24*7)
    return JSONResponse(
        content= {
            "access_token": acc_token,
            "refresh_token": ref_token
        },
        status_code=200
    )

def me(access_token: str = Depends(JWTHandler())):
    user_id = JWTHandler.verifyAccessToken(access_token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="invalid access token")
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    user = user._asdict()
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    if not user["verified"]:
        raise HTTPException(status_code=401, detail="user not verified")
    del user["password"]
    return JSONResponse(
        content=user,
        status_code=200
    )
    
def refreshAccToken(refresh_token: str = Depends(JWTHandler())):
    user_id = JWTHandler.verifyRefreshToken(refresh_token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="invalid refresh token")
    acc_token = JWTHandler.createAccessToken(user_id)
    return JSONResponse(
        content= {
            "access_token": acc_token,
        },
        status_code=200
    )

@auth_router.post("/register", response_model=ResponseModels.UserRegisterResponseModel, responses= ResponseModels.UserRegisterResponseModelResponses)
def register(userInfo: UserModels.CreateUserModel):
    user: User = get_user_by_email(userInfo.email)
    if user is not None:
        raise HTTPException(status_code=409, detail="email already exists")
    hashed_pw = hash_password(userInfo.password)
    userInfo.password = hashed_pw
    user = User(**userInfo.model_dump())
    with get_db_session() as session:
        session.add(user)
        session.commit()
        session.close()
    return JSONResponse(
        content={
            "message": "user created"
        },
        status_code=201
    )
    
def getUser(user_id: int, access_token: str = Depends (JWTHandler())):
    user_id = JWTHandler.verifyAccessToken(access_token)
    user_admin = is_admin_check(user_id)
    if not user_admin:
        raise HTTPException(status_code=403, detail="user is not admin")
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return JSONResponse(
        content=user._asdict(),
        status_code=200
    )

    
def delete_user(user_id: int, access_token: str = Depends(JWTHandler())):
    admin_id = JWTHandler.verifyAccessToken(access_token)
    user_admin = is_admin_check(admin_id)
    if not user_admin:
        raise HTTPException(status_code=403, detail="user is not admin")
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    response = delete_user_by_id(user_id)
    if response is None:
        raise HTTPException(status_code=500, detail="user not deleted")
    response2 = delete_candidate(user_id)
    if response2 is None:
        raise HTTPException(status_code=500, detail="candidate not deleted")
    return JSONResponse(
        content={ "message": "user deleted" },
        status_code=200
    )
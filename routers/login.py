from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from functions import emailIsValid, isValidVerificationCode, sendVerificationCode
import oauth2
import schemas

router = APIRouter(prefix="/api/tracker/login", tags=["Authentication"])

# Login
@router.get("/", response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    if emailIsValid(user_credentials.username):
        #verify password
        
        #retrieve user id / role from db
        userId = 78910
        role = "admin"
        access_token = oauth2.create_access_token(data = {"userId": userId, "role":role})
        return schemas.Token(access_token=access_token, token_type="Bearer")
    else:
        raise HTTPException(status_code=403, detail= "Invalid Credentials")
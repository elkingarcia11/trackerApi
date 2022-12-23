from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from functions import emailIsValid
from oauth2 import create_access_token
from schemas import Token
from database import conn, cursor

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

router = APIRouter(prefix="/api/tracker/login", tags=["Authentication"])

# Login
@router.get("/", response_model=Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    if emailIsValid(user_credentials.username):
        hashed_password = pwd_context.hash(user_credentials.password)
        cursor.execute("""SELECT * FROM users WHERE (username = %s AND password = %s) RETURNING *""", (user_credentials.username, hashed_password))
        user = cursor.fetchone()
        conn.commit()
        if user == None:
            raise HTTPException(status_code=403, detail= "Invalid Credentials")
        else:
            #extract user id and role from user
            userId = 78910
            role = "admin"
            access_token = create_access_token(data = {"userId": userId, "role":role})
            return Token(access_token=access_token, token_type="Bearer")
        # check if email & password exist, if so, return user id and role from db
    else:
        raise HTTPException(status_code=403, detail= "Invalid Credentials")
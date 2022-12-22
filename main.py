from fastapi import FastAPI
import routers.login
import routers.transactions
# from passlib.context import CryptContext
#pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
#hashed_password = pwd_context.hash("password")

app = FastAPI()
app.include_router(routers.login.router)
app.include_router(routers.transactions.router)
from typing import Optional
from pydantic import BaseModel

class Token (BaseModel):
    access_token: str
    token_type: str

class LogInRequest(BaseModel):  
    email: str
    password : str

class TokenData(BaseModel):
    userId : Optional[str] = None
    role : Optional[str] = None

class Transaction(BaseModel):
    id : str
    name : str
    invoice : str
    paid : str
    receipt : str
    date : str

class TransactionRequestResponse(BaseModel):
    status : int
    message : str
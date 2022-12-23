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
    receipt : str
    amount_paid : str
    date_processed : str

class TransactionRequestResponse(BaseModel):
    status : int
    message : str
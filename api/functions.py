from typing import Optional
from pydantic import BaseModel

class Transaction(BaseModel):
    id : str
    name : str
    invoice : str
    paid : str
    receipt : str
    date : str
    
class LogInRequest(BaseModel):  
    email: str
    authenticationCode : Optional[str] = None

def isValidAuthToken(authToken : str): 
    # search db for auth token, if doesn't exist, return False
    # else
    return True

def isValidTransaction(transaction : str):
    # run transaction validation field by field
    # if not valid
        # return false
    # else
    return True

def canAddTransactionToDatabase(transaction: str):
    # check for duplicates or conflits
    # if conflict
        # return false
    #else
    return True

def apiKeyAndEmailExist(apiKey : str, email : str):
    # check if email is valid
    # if not return false
    # else
        # check if api key and email exist in db
        # if either do not
            # return false
        #else
    return True

def isValidVerificationCode(code : str, email : str):
    # if code and email are not valid
        # retrn false
    #else 
    return True

def generateToken():
    token = "randomly generated token"
    return token

def transactionExists(id : str):
    # check if transaction exists
    #if not
        #return false
    #else   
    return True

def fieldsAreValid(transaction : Transaction):
    # check if all fields are valid
    #check if updating creates conflicts
    # if not
     # return false
    #else
    return True
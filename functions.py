from pydantic import BaseModel
from email_validator import validate_email, EmailNotValidError
import yagmail
from decouple import config
import random, string

from schemas import Transaction

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

def emailIsValid(email : str):
    try:
        validation = validate_email(email)
    except:
        return False
    
   
    # check if api key and email exist in db
    # if either do not
        # return false
    return True

def isValidVerificationCode(code : str, email : str):
    # if code and email are not valid
        # retrn false
    #else 
    return True

def isValidAuthToken(authToken : str): 
    # search db for auth token, if doesn't exist, return False
    # else
    return True

def sendVerificationCode(email : str):
    user = config('MAIL_USERNAME')
    app_password = config('APP_PASSWORD') # a token for gmail
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    subject = 'Verification Code'
    content = '{c}'.format(c=code)
    with yagmail.SMTP(user, app_password) as yag:
        yag.send(email, subject, content)

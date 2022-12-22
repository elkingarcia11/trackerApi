from typing import Union
from fastapi import APIRouter, Response, Depends, HTTPException
from functions import Transaction, canAddTransactionToDatabase, fieldsAreValid, isValidAuthToken, isValidTransaction, transactionExists
import oauth2
from schemas import TokenData, TransactionRequestResponse
transactions = [{"id": 1, "name": "Elkin Garcia", "invoice": "123456", "paid": "125", "receipt": "1234219", "date": "2022-12-22"}, {"id": 2, "name": "Elkidsan Garcia", "invoice": "12342156",
                                                                                                                                    "paid": "1325", "receipt": "12341219", "date": "2022-12-20"}, {"id": 3, "name": "Elkin Rodriguez", "invoice": "993829", "paid": "200", "receipt": "123", "date": "2022-12-10"}]

router = APIRouter(prefix="/api/tracker/transactions", tags=['Transactions'])

# Get transactions
@router.get("/")
async def getTransactions(user_credentials: TokenData = Depends(oauth2.get_current_user)):
    print(user_credentials.role)
    if user_credentials.userId is None:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    if user_credentials.role is None:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    return transactions

# Add transaction
@router.post("/", response_model=TransactionRequestResponse)
async def addTransaction(body: Transaction, user_credentials: TokenData = Depends(oauth2.get_current_user)):
    if user_credentials.userId is None:
        return TransactionRequestResponse(status=403, message="Invalid credentials")
    if user_credentials.role is None:
        return TransactionRequestResponse(status=403, message="Invalid credentials")
    if user_credentials.role == "admin":
        if canAddTransactionToDatabase(body):
            if isValidTransaction(body):
                transactions.append(body.dict())
                return TransactionRequestResponse(status=200, message="Successfully added transaction to database" )
            else:
                return TransactionRequestResponse(status=400, message="This is an invalid transaction submission")
        else:
            return TransactionRequestResponse(status=400, message="Could not add transaction to database")
    else:
        return TransactionRequestResponse(status=403, message="Invalid credentials")



# Update transaction
@router.put("/", response_model=TransactionRequestResponse)
async def updateTransaction(body: Transaction, user_credentials: TokenData = Depends(oauth2.get_current_user)):
    if user_credentials.userId is None:
        return TransactionRequestResponse(status=403, message="Invalid credentials")
    if user_credentials.role is None:
        return TransactionRequestResponse(status=403, message="Invalid credentials")
    if user_credentials.role == "admin":
        if transactionExists(body.id):
            if fieldsAreValid(body):
                # update db with new fields
                for i, t in enumerate(transactions):
                    if str(t['id']) == body.id:
                        transactions[i] = body.dict()
                return TransactionRequestResponse(status_code=204, message="Transaction successfully updated!")
            else:
                return TransactionRequestResponse(status=400, message="Fields are invalid so transaction could not be updated")
        else:
            return TransactionRequestResponse(status=404, message="Transaction not found")
    else:
        return TransactionRequestResponse(status=403, message="Invalid credentials")


# Delete transaction(s)
@router.delete("/")
async def deleteTransactions(id : Union[str, None] = None, user_credentials: TokenData = Depends(oauth2.get_current_user)): 
    if user_credentials.userId is None:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    if user_credentials.role is None:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    if user_credentials.role == "admin":
        for i in id:
            if transactionExists(i):
                # remove transaction from db using id
                for t in transactions:
                    if str(t['id']) == i:
                        transactions.remove(t)
    else:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    
    return TransactionRequestResponse(status=200, message="Transaction(s) successfully removed!")
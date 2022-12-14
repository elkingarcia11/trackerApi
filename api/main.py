from fastapi import FastAPI, Response, HTTPException

from api.functions import Transaction, apiKeyAndEmailExist, canAddTransactionToDatabase, fieldsAreValid, generateToken, isValidAuthToken, isValidTransaction, isValidVerificationCode, transactionExists

app = FastAPI()

transactions = [{"id":1,"name":"Elkin Garcia","invoice":"123456","paid":"125","receipt":"1234219","date":"2022-12-22"},{"id":2,"name":"Elkidsan Garcia","invoice":"12342156","paid":"1325","receipt":"12341219","date":"2022-12-20"},{"id":3,"name":"Elkin Rodriguez","invoice":"993829","paid":"200","receipt":"123","date":"2022-12-10"}]

# Get transactions
@app.get("/api/tracker/transactions")
async def getTransactions():
    if isValidAuthToken("authToken"):
        #retrieve transactions from db
        # if unsuccessful throw HTTP EXCEPTION 503
        # else
        return {"transactions":transactions}
    else: 
        raise HTTPException(status_code=401, detail= "Client is not authorized to retrieve this information")

# Add transaction
@app.post("/api/tracker/transactions")
async def addTransaction(body : Transaction):
    if isValidAuthToken("authToken"):
        if isValidTransaction(body.transaction):
            if canAddTransactionToDatabase(body.transaction):
                transactions.append(body.dict())        
                return {"Transaction successfully added!"}
            else:
                raise HTTPException(status_code=409, detail= "Could not add transaction to database")
        else:
            raise HTTPException(status_code=400, detail= "This is an invalid transaction submission")
    else:
        raise HTTPException(status_code=401, detail= "Client is not authorized to process this request")

# Login
@app.get("/api/tracker/login")
async def login(body : LogInRequest):
    if apiKeyAndEmailExist("apiKey", body.email):
        # send verification code
        # store verification code email for a few minutes / limit attempts ??
        return {"SEND VERIFICATION CODE"}
    else:
        raise HTTPException(status_code=401, detail= "User does not exist")

# Authenticate
@app.post("/api/tracker/login")
async def authenticate(body : LogInRequest):
    if apiKeyAndEmailExist("apiKey", body.email):
        if isValidVerificationCode(body.email, body.authenticationCode):
            return generateToken()
        else:
            raise HTTPException(status_code=404, detail= "Incorrect verification code")
    else:
        raise HTTPException(status_code=401, detail= "User does not exist")

# Update transaction
@app.put("/api/tracker/transactions")
async def updateTransaction(body : Transaction):
    if isValidAuthToken("authToken"):
        if transactionExists(id):
            if fieldsAreValid(body):
                # update db with new fields
                for i, t in enumerate(transactions):
                    if str(t['id']) == body.id:
                        transactions[i] = body.dict()
                return Response(status_code=204)
            else:
                raise HTTPException(status_code=400, detail= "Fields are invalid so transaction could not be updated")
        else:
            raise HTTPException(status_code=404, detail= "Transaction not found")
    else:
        raise HTTPException(status_code=401, detail= "Client is not authorized to process this request")


# Delete transaction(s)
@app.delete("/api/tracker/transactions/{id}")
async def deleteTransactions(id : str):
    if isValidAuthToken("authToken"):
        if transactionExists(id):
            # remove transaction from db using id
            for t in transactions:
                if str(t['id']) == id:
                    transactions.remove(t)
                    return Response(status_code=204)
            raise HTTPException(status_code=404, detail= "Transaction not found")
        else:
            raise HTTPException(status_code=404, detail= "Transaction not found")
    else:
        raise HTTPException(status_code=401, detail= "Client is not authorized to process this request")
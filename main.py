from fastapi import FastAPI

app = FastAPI()

# Get transactions
@app.get("/api/tracker/get/transactions")
async def getTransactions():
    return {"message":"header- auth token, -> return all transactions in DB"}

# Login
@app.post("/api/tracker/post/login")
async def login():
    return {"message":"header- api-key, body- email -> return verification code if valid, else return fail"}

# Authenticate
@app.post("/api/tracker/post/auth")
async def authenticate():
    return {"message":"header- api-key, body- email & verification code -> return auth token if valid, else return fail"}

# Delete transaction(s)
@app.delete("/api/tracker/delete/{transactionId}*")
async def deleteTransactions():
    return {"message":"header- auth token body- transaction ids -> return success if valid, else return fail"}

# Update transaction
@app.put("/api/tracker/put/{transactionId}*")
async def updateTransaction():
    return {"message":"header- auth token body- transaction id, fields to update, -> return success if valid, else return fail"}
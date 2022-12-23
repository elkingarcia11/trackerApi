from typing import Union
from fastapi import APIRouter, Depends, HTTPException
from functions import Transaction, isDuplicateTransaction, isValidTransaction, transactionExists
from schemas import TokenData, TransactionRequestResponse
from oauth2 import get_current_user
from database import conn, cursor

#transactions = [{"id": 1, "name": "Elkin Garcia", "invoice": "123456", "paid": "125", "receipt": "1234219", "date": "2022-12-22"}, {"id": 2, "name": "Elkidsan Garcia", "invoice": "12342156",
#                                                                                                                                    "paid": "1325", "receipt": "12341219", "date": "2022-12-20"}, {"id": 3, "name": "Elkin Rodriguez", "invoice": "993829", "paid": "200", "receipt": "123", "date": "2022-12-10"}]
router = APIRouter(prefix="/api/tracker/transactions", tags=['Transactions'])

# Get transactions
@router.get("/", status_code=200)
async def getTransactions(user_credentials: TokenData = Depends(get_current_user)):
    if user_credentials.userId is None:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    if user_credentials.role is None:
        return TransactionRequestResponse(status=403, message="Invalid credentials")
    cursor.execute("""SELECT * FROM transactions """)
    transactions = cursor.fetchall()
    return {"data": transactions}

# Add transaction
@router.post("/", status_code=201)
async def addTransaction(transaction: Transaction, user_credentials: TokenData = Depends(get_current_user)):
    if user_credentials.userId is None:
        return TransactionRequestResponse(status=403, message="Invalid credentials")
    if user_credentials.role is None:
        return TransactionRequestResponse(status=403, message="Invalid credentials")
    if user_credentials.role == "admin":
        # validate fields, check if duplicate, add
        if isValidTransaction(transaction):
            if isDuplicateTransaction(transaction):
                return TransactionRequestResponse(status=400, message="This is a duplicate entry")
            else:
                cursor.execute("""INSERT INTO transactions (name, invoice, receipt, amount_paid, date_processed) VALUES (%s, %s, %s, %s, %s) RETURNING * """, (transaction.name, transaction.invoice, transaction.receipt, transaction.amount_paid, transaction.date_processed))
                new_transaction = cursor.fetchone()
                conn.commit()
                return {"data": new_transaction}

        else:
            return TransactionRequestResponse(status=400, message="Could not add transaction to database")
    else:
        return TransactionRequestResponse(status=403, message="Invalid credentials")


# Update transaction
@router.put("/", status_code=200)
async def updateTransaction(transaction: Transaction, user_credentials: TokenData = Depends(get_current_user)):
    if user_credentials.userId is None:
        return TransactionRequestResponse(status=403, message="Invalid credentials")
    if user_credentials.role is None:
        return TransactionRequestResponse(status=403, message="Invalid credentials")
    if user_credentials.role == "admin":
        if transactionExists(transaction.id):
            # update db with new fields
            # return response
            cursor.execute("""UPDATE transactions SET name = %s, invoice = %s, receipt = %s, amount_paid = %s, date_processed = %s) WHERE id = %s RETURNING *  """, (transaction.name, transaction.invoice, transaction.receipt, transaction.amount_paid, transaction.date_processed, transaction.id))
            updated_transaction = cursor.fetchone()
            conn.commit()
            if updated_transaction == None:
                raise HTTPException(status_code=404, detail="Transaction could not be found and/or updated!")

            return {"data": updated_transaction}
        else:
            return TransactionRequestResponse(status=404, message="Transaction not found")
    else:
        return TransactionRequestResponse(status=403, message="Invalid credentials")

# Delete transaction(s)
@router.delete("/", status_code=204)
async def deleteTransactions(id: Union[str, None] = None, user_credentials: TokenData = Depends(get_current_user)):
    if user_credentials.userId is None:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    if user_credentials.role is None:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    if user_credentials.role == "admin":
        deleted_transactions = [str]
        for i in id:
            cursor.execute("""DELETE FROM transactions WHERE id = %s returning *  """, (i))
            deleted_transaction = cursor.fetchone()
            conn.commit()
            if deleted_transaction == None:
                deleted_transactions.append("ID not found: %s", i)
            else:
                deleted_transactions.append(deleted_transaction)
        return {"Deleted transactions": deleted_transactions}
    else:
        raise HTTPException(status_code=403, detail="Invalid credentials")
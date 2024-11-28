from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import cbe  

app = FastAPI()

# Define a request model to validate input
class TransactionRequest(BaseModel):
    account_number: str
    transaction_number: str


# Define the route to check transaction details
@app.post("/check-transaction")
async def check_transaction(request: TransactionRequest):
    try:
        details = cbe.fetch_transaction_details(request.account_number, request.transaction_number)
        return details
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


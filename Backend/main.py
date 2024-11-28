from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import cbe
import telebirr 

app = FastAPI()

# Define a request model to validate input
class CBETransactionRequest(BaseModel):
    account_number: str
    transaction_number: str

class TelebirrTransactionRequest(BaseModel):
    transaction_number: str


@app.post("/check-cbe")
async def check_transaction(request: CBETransactionRequest):
    try:
        details = cbe.fetch_transaction_details(request.account_number, request.transaction_number)
        return details
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/check-telebirr")
async def check_telebirr_transaction(request: TelebirrTransactionRequest):
    try:
        details = telebirr.get_transaction_details(request.transaction_number)
        return details
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

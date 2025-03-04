from pydantic import BaseModel
from datetime import datetime

class CashResponse(BaseModel):
    amount: float
    updated_at: datetime

class TransactionCreate(BaseModel):
    type: str
    amount: float


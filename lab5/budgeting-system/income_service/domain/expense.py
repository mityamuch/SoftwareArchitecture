from pydantic import BaseModel
from datetime import datetime

class Expense(BaseModel):
    id: int
    user_id: int
    amount: float
    description: str
    date: datetime
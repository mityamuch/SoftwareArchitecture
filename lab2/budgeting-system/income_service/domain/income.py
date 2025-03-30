from pydantic import BaseModel
from datetime import date

class Income(BaseModel):
    id: int
    user_id: int
    amount: float
    description: str
    date: date
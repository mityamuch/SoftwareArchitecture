from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class User(BaseModel):
    id: Optional[int] = None
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    hashed_password: str = Field(..., min_length=8)
    age: Optional[int] = Field(None, ge=0, le=120)
from pydantic import BaseModel
from datetime import datetime
from typing import List

class User(BaseModel):
    
    name: str
    email: str
    gender: str
    phone_number: str
    age: int
    password: str
    created_at: datetime
    updated_at: datetime 
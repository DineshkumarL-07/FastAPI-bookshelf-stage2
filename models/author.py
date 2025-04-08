from pydantic import BaseModel
from datetime import datetime
from typing import List

class Author(BaseModel):
    name: str
    age: int
    gender: str
    awards: List
    created_at: datetime
    updated_at: datetime
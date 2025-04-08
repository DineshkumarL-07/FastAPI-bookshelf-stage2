from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Book(BaseModel):
    title: str
    description: str
    isbn: str
    author_id: str
    category_id: str
    publisher_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime 
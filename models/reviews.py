from pydantic import BaseModel
from datetime import datetime
# from typing import Dict


class Review(BaseModel):
    content: str
    rating: int
    created_by: str
    book_id: str
    created_at: datetime
    updated_at: datetime
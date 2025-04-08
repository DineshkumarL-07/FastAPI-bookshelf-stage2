from pydantic import BaseModel
from datetime import datetime
from typing import List

class Bookstore(BaseModel):
    name: str
    location: str
    book_ids: List[str]
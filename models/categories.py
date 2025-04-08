from pydantic import BaseModel
from datetime import datetime

class Category(BaseModel):
    name: str
    description: str

    
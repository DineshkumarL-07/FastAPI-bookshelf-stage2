from pydantic import BaseModel
from typing import List
from datetime import datetime


class Publisher(BaseModel):
    name: str
    location: str

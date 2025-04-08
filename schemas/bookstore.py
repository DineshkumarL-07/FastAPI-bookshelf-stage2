from pydantic import BaseModel, Field
from typing import Optional, List
# from app_task2.schemas import ProvideResponse

class CreateBookstore(BaseModel):
    name: str = Field(..., examples=["Barnes & Noble"])
    location: str = Field(..., examples=["New York, USA"])

class UpdateBookstore(BaseModel):
    name: Optional[str] = Field(None, examples=["Barnes & Noble Updated"])
    location: Optional[str] = Field(None, examples=["Los Angeles, USA"])

class BookstoreResponse(BaseModel):
    id: str = Field(..., examples=["6683e1a4710824df4e5d76e9"])
    name: str = Field(..., examples=["Barnes & Noble"])
    location: str = Field(..., examples=["New York, USA"])
    books: List[dict] = Field(default_factory=list, examples=[[{"id": "book_id", "name": "Book Title"}]])
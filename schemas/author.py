from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
# from app_task2.schemas import ProvideResponse

class CreateAuthor(BaseModel):
    name: str = Field(..., examples=["Mark Twain"])
    age: int = Field(..., examples=[45])
    gender: str = Field(..., examples=["Male"])
    awards: List[str] = Field(..., examples=[["Best writer of the decade - 2018"]])

class AuthorResponse(BaseModel):
    id: str = Field(..., examples=["6683e1a4710824df4e5d76e9"])
    name: str = Field(..., examples=["Mark Twain"])
    age: int = Field(..., examples=[45])
    gender: str = Field(..., examples=["Male"])
    awards: List[str] = Field(..., examples=[["Best writer of the decade - 2018"]])
    latest_books: List[dict] = Field(default_factory=list, examples=[[{"id": "bookid1", "title": "Book Title"}]])
    total_published: int = Field(..., examples=[10])
    average_rating: float = Field(..., examples=[4.5])
    created_at: datetime = Field(..., examples=[datetime(2023, 10, 1)])
    updated_at: datetime = Field(..., examples=[datetime(2023, 10, 1)])

class UpdateAuthor(BaseModel):
    name: Optional[str] = Field(None, examples=["Samuel Clemens"])
    age: Optional[int] = Field(None, examples=[46])
    gender: Optional[str] = Field(None, examples=["Male"])
    awards: Optional[List[str]] = Field(None, examples=[["Best writer of the decade - 2018"]])
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
# from app_task2.schemas import ProvideResponse

class BookCreate(BaseModel):
    title: str = Field(..., examples=["Harry Porter Chambers of secrets (VOLUME 1)"])
    description: str = Field(..., examples=["This is description about a book."])
    isbn: str = Field(..., examples=["12345678901234"])
    author_id: str = Field(..., examples=["6683e1a4710824df4e5d76e9"])
    category_id: str = Field(..., examples=["6769be7156ca61f944fa3f90"])
    publisher_id: Optional[str] = Field(None, examples=["6683e1a4710824df4e5d76e9"])
    # created_at: datetime = Field(default_factory=datetime.now)
    # updated_at: datetime = Field(default_factory=datetime.now)

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, examples=["Harry Porter Chambers of secrets (VOLUME 1)"])
    description: Optional[str] = Field(None, examples=["This is description about a book."])
    author_id: Optional[str] = Field(None, examples=["6683e1a4710824df4e5d76e9"])
    category_id: Optional[str] = Field(None, examples=["6769be7156ca61f944fa3f90"])
    publisher_id: Optional[str] = Field(None, examples=["6683e1a4710824df4e5d76e9"])

class BookResponse(BaseModel):
    id: str = Field(..., examples=["6683f946ec61bfa6a3c2d7c7"])
    title: str = Field(..., examples=["Harry Porter Chambers of secrets (VOLUME 1)"])
    description: str = Field(..., examples=["This is description about a book."])
    isbn: str = Field(..., examples=["12345678901234"])
    author: dict = Field(..., examples=[{'id': "6683e1a4710824df4e5d76e9", 'name' : 'James'}])
    category: dict = Field(..., examples=[{"id": "6769be7156ca61f944fa3f90","name": "Fiction"}])
    publisher: Optional[dict] = Field(None, examples=[{"id": "6683e1a4710824df4e5d76e9","name": "Penguin Random House"}])
    is_published: bool = Field(..., examples=[False])
    average_rating: Optional[float] = Field(None, examples=[4.5])
    total_reviews: Optional[int] = Field(None, examples=[150]) 
    created_at: datetime = Field(..., examples=[datetime(2023, 10, 1)])
    updated_at: datetime = Field(..., examples=[datetime(2023, 10, 1)])
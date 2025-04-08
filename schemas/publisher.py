from pydantic import BaseModel, Field
from typing import Optional, List
# from app_task2.schemas import ProvideResponse

class CreatePublisher(BaseModel):
    name: str = Field(..., examples=["Penguin Random House"])
    location: str = Field(..., examples=["New York, USA"])

class UpdatePublisher(BaseModel):
    name: Optional[str] = Field(None, examples=["Penguin Random House"])
    location: Optional[str] = Field(None, examples=["Los Angeles, USA"])

class PublisherResponse(BaseModel):
    id: str = Field(..., examples=["6683e1a4710824df4e5d76e9"])
    name: str = Field(..., examples=["Penguin Random House"])
    location: str = Field(..., examples=["New York, USA"])
    books: List[dict] = Field(default_factory=list, examples=[[{"id": "book_id", "name": "Book Title"}]])
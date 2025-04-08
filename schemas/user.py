from typing import Optional, List, Any
from pydantic import BaseModel, Field
from datetime import datetime
# from app_task2.schemas import ProvideResponse

class CreateUser(BaseModel):
    name :str = Field(...,examples=["uday kiran reddy"])
    email: str = Field(..., examples = ["uday@zysec.ai"])
    gender: str  = Field(...,examples = ['Male'])
    phone_number: str  = Field(...,examples = ['9998844333'])
    age: int = Field(...,examples = [24])
    password: str = Field(...,examples = ['strongpassword123'])
    
class UserResponse(BaseModel):
    id: str = Field(..., examples=["6683e1a4710824df4e5d76e9"])
    name :str = Field(...,examples=["uday kiran reddy"])
    email: str = Field(..., examples = ["uday@zysec.ai"])
    gender: str  = Field(...,examples = ['Male'])
    phone_number: str  = Field(...,examples = ['9998844333'])
    age: int = Field(...,examples = [24])
    favorite_books: List = Field(default_factory=list, examples=[[{"id": "bookid1", "title": "Book Title"}]])
    total_reviews: int = Field(..., examples=[10])
    created_at: datetime = Field(..., examples=["2023-10-01T12:00:00Z"])
    updated_at: datetime = Field(..., examples=["2023-10-01T12:00:00Z"])

class UpdateUser(BaseModel):
    name :Optional[str] = Field(None,examples=["uday kiran reddy"])
    email: Optional[str] = Field(None, examples = ["uday@zysec.ai"])
    gender: Optional[str]  = Field(None,examples = ['udayreddy_26'])
    age: Optional[int] = Field(None,examples = [24])
    phone_number: Optional[str]  = Field(None,examples = ['udayreddy_26'])
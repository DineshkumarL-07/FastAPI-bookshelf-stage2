from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
# from app_task2.schemas import ProvideResponse

class CreateReview(BaseModel):
    content: str = Field(..., examples=["An outstanding work of literature!"])
    rating: int = Field(..., examples=[5])
    created_by: str = Field(..., examples=["67a62fab1c388e002d06805d"])  
    book_id: str = Field(..., examples=["67a5c096118d563cb5900e18"])        

class UpdateReview(BaseModel):
    content: Optional[str] = Field(None, examples=["A timeless classic that leaves a lasting impression."])
    rating: Optional[int] = Field(None, examples=[5])

class ReviewResponse(BaseModel):
    id: str = Field(..., examples=["67a5c096118d563cb5900e18"])
    content: str = Field(..., examples=["An outstanding work of literature!"])
    rating: int = Field(..., examples=[5])
    created_by: dict = Field(..., examples=[{"id": "67a62fab1c388e002d06805d", "name": "John Doe"}])
    book_id: dict = Field(..., examples=[{"id": "67a5c096118d563cb5900e18", "name": "Harry Potter and the Chamber of Secrets"}])
    review_details: dict = Field(..., examples=[{
        "likes": 120,
        "comments": [
            {
                "id": "6683e1a4710824df4e5d76e9",
                "user": "John Doe",
                "content": "Great review!"
            }
        ]
    }])
    created_at: datetime = Field(..., examples=[datetime(2023, 10, 1)])
    updated_at: datetime = Field(..., examples=[datetime(2023, 10, 1)])
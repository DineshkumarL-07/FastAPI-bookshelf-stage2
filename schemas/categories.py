from pydantic import BaseModel, Field
from typing import Optional
# from app_task2.schemas import ProvideResponse

class CreateCategory(BaseModel):
    name: str = Field(..., examples=["Fiction"])
    description: str = Field(..., examples=["Fictional books and stories."])

class UpdateCategory(BaseModel):
    name: Optional[str] = Field(None, examples=["Non-Fiction"])
    description: Optional[str] = Field(None, examples=["Real stories and factual content."])

class CategoryResponse(BaseModel):
    id: str = Field(..., examples=["6769be7156ca61f944fa3f90"])
    name: str = Field(..., examples=["Fiction"])
    description: str = Field(..., examples=["Fictional books and stories."])
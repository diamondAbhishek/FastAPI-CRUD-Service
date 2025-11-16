"""
Pydantic Schemas for Request/Response Validation
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class BookBase(BaseModel):
    """Base schema for Book with common fields"""
    title: str = Field(..., min_length=1, max_length=200, description="Book title")
    description: Optional[str] = Field(None, max_length=1000, description="Book description")
    author: str = Field(..., min_length=1, max_length=100, description="Book author")

    model_config = ConfigDict(from_attributes=True)


class BookCreate(BookBase):
    """Schema for creating a new book"""
    pass


class BookUpdate(BaseModel):
    """Schema for updating a book (all fields optional)"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Book title")
    description: Optional[str] = Field(None, max_length=1000, description="Book description")
    author: Optional[str] = Field(None, min_length=1, max_length=100, description="Book author")

    model_config = ConfigDict(from_attributes=True)


class BookResponse(BookBase):
    """Schema for book response"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BookListResponse(BaseModel):
    """Schema for paginated book list response"""
    items: list[BookResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


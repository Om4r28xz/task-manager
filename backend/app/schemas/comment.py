from pydantic import BaseModel, Field
from datetime import datetime


class CommentBase(BaseModel):
    """Base comment schema"""
    content: str = Field(..., min_length=1)
    task_id: str


class CommentCreate(CommentBase):
    """Schema for creating a comment"""
    pass


class Comment(CommentBase):
    """Comment schema for API responses"""
    id: str = Field(alias="_id")
    user_id: str
    username: str  # Joined from user
    created_at: datetime
    
    class Config:
        populate_by_name = True

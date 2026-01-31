from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema"""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=3, max_length=100)


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    email: Optional[str] = Field(None, min_length=3, max_length=100)
    password: Optional[str] = Field(None, min_length=6)


class UserInDB(UserBase):
    """User schema as stored in database"""
    id: str = Field(alias="_id")
    hashed_password: str
    created_at: datetime
    
    class Config:
        populate_by_name = True


class User(UserBase):
    """User schema for API responses"""
    id: str = Field(alias="_id")
    created_at: datetime
    
    class Config:
        populate_by_name = True

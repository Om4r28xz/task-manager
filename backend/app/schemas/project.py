from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProjectBase(BaseModel):
    """Base project schema"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    """Schema for creating a project"""
    pass


class ProjectUpdate(BaseModel):
    """Schema for updating a project"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None


class Project(ProjectBase):
    """Project schema for API responses"""
    id: str = Field(alias="_id")
    created_by: str
    created_at: datetime
    
    class Config:
        populate_by_name = True

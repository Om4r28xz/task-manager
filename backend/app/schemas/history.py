from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class HistoryAction(str, Enum):
    """History action enumeration"""
    CREATED = "CREATED"
    STATUS_CHANGED = "STATUS_CHANGED"
    TITLE_CHANGED = "TITLE_CHANGED"
    ASSIGNED = "ASSIGNED"
    PRIORITY_CHANGED = "PRIORITY_CHANGED"
    UPDATED = "UPDATED"
    DELETED = "DELETED"


class HistoryBase(BaseModel):
    """Base history schema"""
    action: HistoryAction
    old_value: Optional[str] = None
    new_value: Optional[str] = None


class HistoryCreate(HistoryBase):
    """Schema for creating a history entry"""
    task_id: str
    user_id: str


class History(HistoryBase):
    """History schema for API responses"""
    id: str = Field(alias="_id")
    task_id: str
    user_id: str
    username: str  # Joined from user
    timestamp: datetime
    
    class Config:
        populate_by_name = True

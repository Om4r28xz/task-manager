from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class NotificationType(str, Enum):
    """Notification type enumeration"""
    TASK_ASSIGNED = "task_assigned"
    TASK_UPDATED = "task_updated"
    TASK_COMPLETED = "task_completed"
    COMMENT_ADDED = "comment_added"


class NotificationBase(BaseModel):
    """Base notification schema"""
    message: str
    type: NotificationType


class NotificationCreate(NotificationBase):
    """Schema for creating a notification"""
    user_id: str


class Notification(NotificationBase):
    """Notification schema for API responses"""
    id: str = Field(alias="_id")
    user_id: str
    read: bool = False
    created_at: datetime
    
    class Config:
        populate_by_name = True

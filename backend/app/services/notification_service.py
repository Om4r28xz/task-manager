from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.notification_repository import NotificationRepository
from typing import List


class NotificationService:
    """Service for notification-related business logic"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.notification_repo = NotificationRepository(db)
    
    async def get_user_notifications(self, user_id: str, unread_only: bool = False) -> List[dict]:
        """Get notifications for a user"""
        return await self.notification_repo.get_by_user(user_id, unread_only)
    
    async def mark_as_read(self, notification_id: str) -> bool:
        """Mark a notification as read"""
        return await self.notification_repo.mark_as_read(notification_id)
    
    async def mark_all_as_read(self, user_id: str) -> bool:
        """Mark all notifications for a user as read"""
        return await self.notification_repo.mark_all_as_read(user_id)

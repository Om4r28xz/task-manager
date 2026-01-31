from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from datetime import datetime
from bson import ObjectId


class NotificationRepository:
    """Repository for Notification data operations"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.notifications
    
    async def create_indexes(self):
        """Create indexes for the notifications collection"""
        await self.collection.create_index("user_id")
        await self.collection.create_index("read")
        await self.collection.create_index("created_at")
    
    async def create(self, notification_data: dict) -> dict:
        """Create a new notification"""
        notification_data["read"] = False
        notification_data["created_at"] = datetime.utcnow()
        result = await self.collection.insert_one(notification_data)
        notification_data["_id"] = str(result.inserted_id)
        return notification_data
    
    async def get_by_user(self, user_id: str, unread_only: bool = False) -> List[dict]:
        """Get notifications for a user"""
        query = {"user_id": user_id}
        if unread_only:
            query["read"] = False
        
        notifications = []
        cursor = self.collection.find(query).sort("created_at", -1)
        async for notification in cursor:
            notification["_id"] = str(notification["_id"])
            notifications.append(notification)
        return notifications
    
    async def mark_as_read(self, notification_id: str) -> bool:
        """Mark a notification as read"""
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(notification_id)},
                {"$set": {"read": True}}
            )
            return result.modified_count > 0
        except:
            return False
    
    async def mark_all_as_read(self, user_id: str) -> bool:
        """Mark all notifications for a user as read"""
        result = await self.collection.update_many(
            {"user_id": user_id, "read": False},
            {"$set": {"read": True}}
        )
        return result.modified_count > 0
    
    async def delete(self, notification_id: str) -> bool:
        """Delete a notification"""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(notification_id)})
            return result.deleted_count > 0
        except:
            return False

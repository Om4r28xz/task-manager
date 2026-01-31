from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from datetime import datetime
from bson import ObjectId


class CommentRepository:
    """Repository for Comment data operations"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.comments
    
    async def create_indexes(self):
        """Create indexes for the comments collection"""
        await self.collection.create_index("task_id")
        await self.collection.create_index("created_at")
    
    async def create(self, comment_data: dict) -> dict:
        """Create a new comment"""
        comment_data["created_at"] = datetime.utcnow()
        result = await self.collection.insert_one(comment_data)
        comment_data["_id"] = str(result.inserted_id)
        return comment_data
    
    async def get_by_task(self, task_id: str) -> List[dict]:
        """Get all comments for a task"""
        comments = []
        cursor = self.collection.find({"task_id": task_id}).sort("created_at", 1)
        async for comment in cursor:
            comment["_id"] = str(comment["_id"])
            comments.append(comment)
        return comments
    
    async def delete(self, comment_id: str) -> bool:
        """Delete a comment"""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(comment_id)})
            return result.deleted_count > 0
        except:
            return False

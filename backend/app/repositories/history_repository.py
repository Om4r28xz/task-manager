from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional
from datetime import datetime
from bson import ObjectId


class HistoryRepository:
    """Repository for History/Audit log data operations"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.history
    
    async def create_indexes(self):
        """Create indexes for the history collection"""
        await self.collection.create_index("task_id")
        await self.collection.create_index("timestamp")
        await self.collection.create_index([("task_id", 1), ("timestamp", -1)])
    
    async def create(self, history_data: dict) -> dict:
        """Create a new history entry"""
        history_data["timestamp"] = datetime.utcnow()
        result = await self.collection.insert_one(history_data)
        history_data["_id"] = str(result.inserted_id)
        return history_data
    
    async def get_by_task(self, task_id: str) -> List[dict]:
        """Get history entries for a specific task"""
        history = []
        cursor = self.collection.find({"task_id": task_id}).sort("timestamp", -1)
        async for entry in cursor:
            entry["_id"] = str(entry["_id"])
            history.append(entry)
        return history
    
    async def get_all(self, limit: int = 100) -> List[dict]:
        """Get all recent history entries"""
        history = []
        cursor = self.collection.find({}).sort("timestamp", -1).limit(limit)
        async for entry in cursor:
            entry["_id"] = str(entry["_id"])
            history.append(entry)
        return history
    
    async def delete_by_task(self, task_id: str) -> bool:
        """Delete all history entries for a task"""
        result = await self.collection.delete_many({"task_id": task_id})
        return result.deleted_count > 0

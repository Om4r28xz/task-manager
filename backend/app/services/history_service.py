from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.history_repository import HistoryRepository
from app.repositories.user_repository import UserRepository
from typing import List


class HistoryService:
    """Service for history/audit log business logic"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.history_repo = HistoryRepository(db)
        self.user_repo = UserRepository(db)
    
    async def get_task_history(self, task_id: str) -> List[dict]:
        """Get history for a specific task with user details"""
        history = await self.history_repo.get_by_task(task_id)
        
        # Enrich with user information
        for entry in history:
            user = await self.user_repo.find_by_id(entry["user_id"])
            entry["username"] = user["username"] if user else "Unknown"
        
        return history
    
    async def get_all_history(self, limit: int = 100) -> List[dict]:
        """Get all recent history entries with user details"""
        history = await self.history_repo.get_all(limit)
        
        # Enrich with user information
        for entry in history:
            user = await self.user_repo.find_by_id(entry["user_id"])
            entry["username"] = user["username"] if user else "Unknown"
        
        return history

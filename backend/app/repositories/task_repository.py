from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId


class TaskRepository:
    """Repository for Task data operations"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.tasks
    
    async def create_indexes(self):
        """Create indexes for the tasks collection"""
        await self.collection.create_index("status")
        await self.collection.create_index("priority")
        await self.collection.create_index("project_id")
        await self.collection.create_index("assigned_to")
        await self.collection.create_index("due_date")
        await self.collection.create_index("created_at")
    
    async def create(self, task_data: dict) -> dict:
        """Create a new task"""
        task_data["created_at"] = datetime.utcnow()
        task_data["updated_at"] = datetime.utcnow()
        result = await self.collection.insert_one(task_data)
        task_data["_id"] = str(result.inserted_id)
        return task_data
    
    async def find_by_id(self, task_id: str) -> Optional[dict]:
        """Find a task by ID"""
        try:
            task = await self.collection.find_one({"_id": ObjectId(task_id)})
            if task:
                task["_id"] = str(task["_id"])
            return task
        except:
            return None
    
    async def get_all(self) -> List[dict]:
        """Get all tasks"""
        tasks = []
        cursor = self.collection.find({})
        async for task in cursor:
            task["_id"] = str(task["_id"])
            tasks.append(task)
        return tasks
    
    async def update(self, task_id: str, update_data: dict) -> bool:
        """Update a task"""
        try:
            update_data["updated_at"] = datetime.utcnow()
            result = await self.collection.update_one(
                {"_id": ObjectId(task_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except:
            return False
    
    async def delete(self, task_id: str) -> bool:
        """Delete a task"""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(task_id)})
            return result.deleted_count > 0
        except:
            return False
    
    async def search(self, filters: Dict[str, Any]) -> List[dict]:
        """Search tasks with filters"""
        query = {}
        
        # Text search in title and description
        if "text" in filters and filters["text"]:
            query["$or"] = [
                {"title": {"$regex": filters["text"], "$options": "i"}},
                {"description": {"$regex": filters["text"], "$options": "i"}}
            ]
        
        # Filter by status
        if "status" in filters and filters["status"]:
            query["status"] = filters["status"]
        
        # Filter by priority
        if "priority" in filters and filters["priority"]:
            query["priority"] = filters["priority"]
        
        # Filter by project
        if "project_id" in filters and filters["project_id"]:
            query["project_id"] = filters["project_id"]
        
        # Filter by assigned user
        if "assigned_to" in filters and filters["assigned_to"]:
            query["assigned_to"] = filters["assigned_to"]
        
        tasks = []
        cursor = self.collection.find(query)
        async for task in cursor:
            task["_id"] = str(task["_id"])
            tasks.append(task)
        return tasks
    
    async def get_by_project(self, project_id: str) -> List[dict]:
        """Get all tasks for a project"""
        tasks = []
        cursor = self.collection.find({"project_id": project_id})
        async for task in cursor:
            task["_id"] = str(task["_id"])
            tasks.append(task)
        return tasks
    
    async def get_by_user(self, user_id: str) -> List[dict]:
        """Get all tasks assigned to a user"""
        tasks = []
        cursor = self.collection.find({"assigned_to": user_id})
        async for task in cursor:
            task["_id"] = str(task["_id"])
            tasks.append(task)
        return tasks

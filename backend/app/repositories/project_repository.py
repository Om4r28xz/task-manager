from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional
from datetime import datetime
from bson import ObjectId


class ProjectRepository:
    """Repository for Project data operations"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.projects
    
    async def create_indexes(self):
        """Create indexes for the projects collection"""
        await self.collection.create_index("name")
        await self.collection.create_index("created_by")
    
    async def create(self, project_data: dict) -> dict:
        """Create a new project"""
        project_data["created_at"] = datetime.utcnow()
        result = await self.collection.insert_one(project_data)
        project_data["_id"] = str(result.inserted_id)
        return project_data
    
    async def find_by_id(self, project_id: str) -> Optional[dict]:
        """Find a project by ID"""
        try:
            project = await self.collection.find_one({"_id": ObjectId(project_id)})
            if project:
                project["_id"] = str(project["_id"])
            return project
        except:
            return None
    
    async def find_by_name(self, name: str) -> Optional[dict]:
        """Find a project by name"""
        project = await self.collection.find_one({"name": name})
        if project:
            project["_id"] = str(project["_id"])
        return project
    
    async def get_all(self) -> List[dict]:
        """Get all projects"""
        projects = []
        cursor = self.collection.find({})
        async for project in cursor:
            project["_id"] = str(project["_id"])
            projects.append(project)
        return projects
    
    async def update(self, project_id: str, update_data: dict) -> bool:
        """Update a project"""
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(project_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except:
            return False
    
    async def delete(self, project_id: str) -> bool:
        """Delete a project"""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(project_id)})
            return result.deleted_count > 0
        except:
            return False

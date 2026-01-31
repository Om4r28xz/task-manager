from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate
from typing import List, Optional


class ProjectService:
    """Service for project-related business logic"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.project_repo = ProjectRepository(db)
    
    async def create_project(self, project_data: ProjectCreate, user_id: str) -> dict:
        """Create a new project"""
        # Check if project with same name exists
        existing = await self.project_repo.find_by_name(project_data.name)
        if existing:
            raise ValueError("Project with this name already exists")
        
        project_dict = project_data.model_dump()
        project_dict["created_by"] = user_id
        
        return await self.project_repo.create(project_dict)
    
    async def get_all_projects(self) -> List[dict]:
        """Get all projects"""
        return await self.project_repo.get_all()
    
    async def get_project(self, project_id: str) -> Optional[dict]:
        """Get a project by ID"""
        return await self.project_repo.find_by_id(project_id)
    
    async def update_project(self, project_id: str, project_data: ProjectUpdate) -> bool:
        """Update a project"""
        update_dict = project_data.model_dump(exclude_unset=True)
        if not update_dict:
            return False
        
        return await self.project_repo.update(project_id, update_dict)
    
    async def delete_project(self, project_id: str) -> bool:
        """Delete a project"""
        return await self.project_repo.delete(project_id)

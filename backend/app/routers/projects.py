from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_database
from app.services.project_service import ProjectService
from app.repositories.user_repository import UserRepository
from app.schemas.project import Project, ProjectCreate, ProjectUpdate
from app.routers.auth import get_current_user
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

router = APIRouter(prefix="/api/projects", tags=["Projects"])


@router.post("", response_model=Project, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create a new project"""
    project_service = ProjectService(db)
    
    try:
        project = await project_service.create_project(project_data, current_user["_id"])
        return project
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("", response_model=List[Project])
async def get_all_projects(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all projects"""
    project_service = ProjectService(db)
    projects = await project_service.get_all_projects()
    return projects


@router.get("/{project_id}", response_model=Project)
async def get_project(
    project_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get a specific project"""
    project_service = ProjectService(db)
    project = await project_service.get_project(project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return project


@router.put("/{project_id}", response_model=dict)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update a project"""
    project_service = ProjectService(db)
    success = await project_service.update_project(project_id, project_data)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or no changes made"
        )
    
    return {"message": "Project updated successfully"}


@router.delete("/{project_id}", response_model=dict)
async def delete_project(
    project_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Delete a project"""
    project_service = ProjectService(db)
    success = await project_service.delete_project(project_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return {"message": "Project deleted successfully"}

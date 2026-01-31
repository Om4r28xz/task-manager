from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.database import get_database
from app.services.task_service import TaskService
from app.schemas.task import Task, TaskCreate, TaskUpdate, TaskWithDetails
from app.routers.auth import get_current_user
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create a new task"""
    task_service = TaskService(db)
    task = await task_service.create_task(task_data, current_user["_id"])
    return task


@router.get("", response_model=List[TaskWithDetails])
async def get_all_tasks(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all tasks with details"""
    task_service = TaskService(db)
    tasks = await task_service.get_tasks_with_details()
    return tasks


@router.get("/search", response_model=List[dict])
async def search_tasks(
    text: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    project_id: Optional[str] = Query(None),
    assigned_to: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Search tasks with filters"""
    task_service = TaskService(db)
    
    filters = {}
    if text:
        filters["text"] = text
    if status:
        filters["status"] = status
    if priority:
        filters["priority"] = priority
    if project_id:
        filters["project_id"] = project_id
    if assigned_to:
        filters["assigned_to"] = assigned_to
    
    tasks = await task_service.search_tasks(filters)
    return tasks


@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get a specific task"""
    task_service = TaskService(db)
    task = await task_service.get_task(task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return task


@router.put("/{task_id}", response_model=dict)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update a task"""
    task_service = TaskService(db)
    success = await task_service.update_task(task_id, task_data, current_user["_id"])
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or no changes made"
        )
    
    return {"message": "Task updated successfully"}


@router.delete("/{task_id}", response_model=dict)
async def delete_task(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Delete a task"""
    task_service = TaskService(db)
    success = await task_service.delete_task(task_id, current_user["_id"])
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return {"message": "Task deleted successfully"}

from fastapi import APIRouter, Depends, Query
from app.database import get_database
from app.services.stats_service import StatsService
from app.repositories.user_repository import UserRepository
from app.routers.auth import get_current_user
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict, Any, List

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/stats", response_model=Dict[str, Any])
async def get_statistics(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get comprehensive task statistics"""
    stats_service = StatsService(db)
    stats = await stats_service.get_task_statistics()
    return stats


@router.get("/generate", response_model=Dict[str, Any])
async def generate_report(
    report_type: str = Query(..., description="Type of report: tasks, projects, users"),
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Generate a report based on type"""
    stats_service = StatsService(db)
    
    if report_type == "tasks":
        data = await stats_service.get_tasks_by_status()
        return {"type": "tasks", "data": data}
    
    elif report_type == "projects":
        data = await stats_service.get_tasks_by_project()
        return {"type": "projects", "data": data}
    
    elif report_type == "users":
        data = await stats_service.get_tasks_by_user()
        return {"type": "users", "data": data}
    
    else:
        return {"error": "Invalid report type"}


@router.get("/users", response_model=List[Dict[str, str]])
async def get_users_list(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get list of all users for dropdowns"""
    user_repo = UserRepository(db)
    users = await user_repo.get_all()
    
    return [
        {"id": user["_id"], "username": user["username"]}
        for user in users
    ]

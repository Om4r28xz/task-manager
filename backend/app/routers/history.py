from fastapi import APIRouter, Depends, Query
from app.database import get_database
from app.services.history_service import HistoryService
from app.schemas.history import History
from app.routers.auth import get_current_user
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

router = APIRouter(prefix="/api/history", tags=["History"])


@router.get("/task/{task_id}", response_model=List[History])
async def get_task_history(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get history entries for a specific task"""
    history_service = HistoryService(db)
    history = await history_service.get_task_history(task_id)
    return history


@router.get("", response_model=List[History])
async def get_all_history(
    limit: int = Query(100, le=500),
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all recent history entries"""
    history_service = HistoryService(db)
    history = await history_service.get_all_history(limit)
    return history

from fastapi import APIRouter, Depends, Query
from app.database import get_database
from app.services.notification_service import NotificationService
from app.schemas.notification import Notification
from app.routers.auth import get_current_user
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


@router.get("", response_model=List[Notification])
async def get_notifications(
    unread_only: bool = Query(False),
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get notifications for the current user"""
    notification_service = NotificationService(db)
    notifications = await notification_service.get_user_notifications(
        current_user["_id"],
        unread_only
    )
    return notifications


@router.post("/{notification_id}/read", response_model=dict)
async def mark_notification_read(
    notification_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Mark a notification as read"""
    notification_service = NotificationService(db)
    success = await notification_service.mark_as_read(notification_id)
    
    if success:
        return {"message": "Notification marked as read"}
    return {"message": "Notification not found"}


@router.post("/read-all", response_model=dict)
async def mark_all_notifications_read(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Mark all notifications as read for the current user"""
    notification_service = NotificationService(db)
    await notification_service.mark_all_as_read(current_user["_id"])
    return {"message": "All notifications marked as read"}

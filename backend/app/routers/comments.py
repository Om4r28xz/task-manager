from fastapi import APIRouter, Depends, status
from app.database import get_database
from app.services.comment_service import CommentService
from app.schemas.comment import Comment, CommentCreate
from app.routers.auth import get_current_user
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

router = APIRouter(prefix="/api/comments", tags=["Comments"])


@router.post("", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create a new comment"""
    comment_service = CommentService(db)
    comment = await comment_service.create_comment(comment_data, current_user["_id"])
    
    # Add username to response
    comment["username"] = current_user["username"]
    return comment


@router.get("/task/{task_id}", response_model=List[Comment])
async def get_task_comments(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all comments for a task"""
    comment_service = CommentService(db)
    comments = await comment_service.get_comments_by_task(task_id)
    return comments

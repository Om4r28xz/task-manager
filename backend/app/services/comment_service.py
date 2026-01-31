from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.comment_repository import CommentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.comment import CommentCreate
from typing import List


class CommentService:
    """Service for comment-related business logic"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.comment_repo = CommentRepository(db)
        self.user_repo = UserRepository(db)
    
    async def create_comment(self, comment_data: CommentCreate, user_id: str) -> dict:
        """Create a new comment"""
        comment_dict = comment_data.model_dump()
        comment_dict["user_id"] = user_id
        
        return await self.comment_repo.create(comment_dict)
    
    async def get_comments_by_task(self, task_id: str) -> List[dict]:
        """Get all comments for a task with user details"""
        comments = await self.comment_repo.get_by_task(task_id)
        
        # Enrich with user information
        for comment in comments:
            user = await self.user_repo.find_by_id(comment["user_id"])
            comment["username"] = user["username"] if user else "Unknown"
        
        return comments

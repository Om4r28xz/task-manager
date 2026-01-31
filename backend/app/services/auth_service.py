from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.user_repository import UserRepository
from app.utils.security import verify_password, get_password_hash, create_access_token
from app.schemas.user import UserCreate, User
from typing import Optional
from datetime import timedelta


class AuthService:
    """Service for authentication operations"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.user_repo = UserRepository(db)
    
    async def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        """Authenticate a user with username and password"""
        user = await self.user_repo.find_by_username(username)
        if not user:
            return None
        
        if not verify_password(password, user["hashed_password"]):
            return None
        
        return user
    
    async def create_token(self, user: dict) -> str:
        """Create an access token for a user"""
        token_data = {
            "sub": user["username"],
            "user_id": user["_id"]
        }
        return create_access_token(token_data)
    
    async def register_user(self, user_data: UserCreate) -> dict:
        """Register a new user"""
        # Check if user already exists
        existing_user = await self.user_repo.find_by_username(user_data.username)
        if existing_user:
            raise ValueError("Username already exists")
        
        existing_email = await self.user_repo.find_by_email(user_data.email)
        if existing_email:
            raise ValueError("Email already exists")
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user
        user_dict = {
            "username": user_data.username,
            "email": user_data.email,
            "hashed_password": hashed_password
        }
        
        return await self.user_repo.create(user_dict)
    
    async def get_current_user(self, username: str) -> Optional[dict]:
        """Get current user by username"""
        return await self.user_repo.find_by_username(username)

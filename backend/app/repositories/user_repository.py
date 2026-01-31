from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional
from datetime import datetime
from bson import ObjectId


class UserRepository:
    """Repository for User data operations"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.users
    
    async def create_indexes(self):
        """Create indexes for the users collection"""
        await self.collection.create_index("username", unique=True)
        await self.collection.create_index("email", unique=True)
    
    async def create(self, user_data: dict) -> dict:
        """Create a new user"""
        user_data["created_at"] = datetime.utcnow()
        result = await self.collection.insert_one(user_data)
        user_data["_id"] = str(result.inserted_id)
        return user_data
    
    async def find_by_username(self, username: str) -> Optional[dict]:
        """Find a user by username"""
        user = await self.collection.find_one({"username": username})
        if user:
            user["_id"] = str(user["_id"])
        return user
    
    async def find_by_id(self, user_id: str) -> Optional[dict]:
        """Find a user by ID"""
        try:
            user = await self.collection.find_one({"_id": ObjectId(user_id)})
            if user:
                user["_id"] = str(user["_id"])
            return user
        except:
            return None
    
    async def find_by_email(self, email: str) -> Optional[dict]:
        """Find a user by email"""
        user = await self.collection.find_one({"email": email})
        if user:
            user["_id"] = str(user["_id"])
        return user
    
    async def get_all(self) -> List[dict]:
        """Get all users"""
        users = []
        cursor = self.collection.find({})
        async for user in cursor:
            user["_id"] = str(user["_id"])
            users.append(user)
        return users
    
    async def update(self, user_id: str, update_data: dict) -> bool:
        """Update a user"""
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except:
            return False
    
    async def delete(self, user_id: str) -> bool:
        """Delete a user"""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except:
            return False

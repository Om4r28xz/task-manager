from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import settings


class Database:
    """MongoDB database connection manager"""
    
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None


db_instance = Database()


async def connect_to_mongo():
    """Create database connection"""
    db_instance.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db_instance.db = db_instance.client[settings.MONGODB_DB_NAME]
    print(f"Connected to MongoDB: {settings.MONGODB_DB_NAME}")


async def close_mongo_connection():
    """Close database connection"""
    if db_instance.client:
        db_instance.client.close()
        print("Closed MongoDB connection")


def get_database() -> AsyncIOMotorDatabase:
    """Get database instance"""
    return db_instance.db

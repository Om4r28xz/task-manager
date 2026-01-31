import os
from dotenv import load_dotenv
from typing import List

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables"""
    
    # MongoDB Configuration
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "task_manager")
    
    # JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS Configuration  
    CORS_ORIGINS: List[str] = os.getenv(
        "CORS_ORIGINS", 
        "http://localhost:5173,http://localhost:3000"
    ).split(",")
    
    # Application Configuration
    APP_NAME: str = os.getenv("APP_NAME", "Task Manager API")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")


settings = Settings()

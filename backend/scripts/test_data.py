"""
Test script to check notifications and comments in the database
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.append(str(Path(__file__).parent.parent))

from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings


async def check_data():
    # Connect to MongoDB
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    
    print("=" * 60)
    print("CHECKING DATABASE DATA")
    print("=" * 60)
    
    # Check notifications
    print("\nNOTIFICATIONS:")
    print("-" * 60)
    notifications = []
    async for notif in db.notifications.find():
        notifications.append(notif)
        print(f"  ID: {notif['_id']}")
        print(f"  User ID: {notif['user_id']}")
        print(f"  Message: {notif['message']}")
        print(f"  Read: {notif['read']}")
        print(f"  Type: {notif['type']}")
        print("-" * 60)
    
    print(f"\nTotal Notifications: {len(notifications)}")
    
    # Check comments  
    print("\nCOMMENTS:")
    print("-" * 60)
    comments = []
    async for comment in db.comments.find():
        comments.append(comment)
        print(f"  ID: {comment['_id']}")
        print(f"  Task ID: {comment['task_id']}")
        print(f"  User ID: {comment['user_id']}")
        print(f"  Content: {comment['content']}")
        print("-" * 60)
    
    print(f"\nTotal Comments: {len(comments)}")
    
    # Check tasks (to get task IDs)
    print("\nTASKS:")
    print("-" * 60)
    tasks = []
    async for task in db.tasks.find():
        tasks.append(task)
        print(f"  ID: {task['_id']}")
        print(f"  Title: {task['title']}")
        print("-" * 60)
    
    print(f"\nTotal Tasks: {len(tasks)}")
    
    # Check users
    print("\nUSERS:")
    print("-" * 60)
    users = []
    async for user in db.users.find():
        users.append(user)
        print(f"  ID: {user['_id']}")
        print(f"  Username: {user['username']}")
        print("-" * 60)
    
    print(f"\nTotal Users: {len(users)}")
    
    client.close()


if __name__ == "__main__":
    asyncio.run(check_data())

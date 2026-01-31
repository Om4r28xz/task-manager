import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def main():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["task_manager"]
    
    # Count documents
    notif_count = await db.notifications.count_documents({})
    comment_count = await db.comments.count_documents({})
    task_count = await db.tasks.count_documents({})
    
    print(f"Notifications: {notif_count}")
    print(f"Comments: {comment_count}")
    print(f"Tasks: {task_count}")
    
    # Get first task and comment for testing
    if task_count > 0:
        task = await db.tasks.find_one()
        print(f"\nFirst Task ID: {task['_id']}")
        
    if comment_count > 0:
        comment = await db.comments.find_one()
        print(f"First Comment Task ID: {comment['task_id']}")
        print(f"Comment Content: {comment['content']}")
    
    if notif_count > 0:
        notif = await db.notifications.find_one()
        print(f"\nFirst Notification User ID: {notif['user_id']}")
        print(f"Notification Message: {notif['message']}")
    
    client.close()

asyncio.run(main())

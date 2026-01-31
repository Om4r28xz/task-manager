from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.user_repository import UserRepository
from app.repositories.history_repository import HistoryRepository
from app.repositories.notification_repository import NotificationRepository
from app.schemas.task import TaskCreate, TaskUpdate, TaskWithDetails
from app.schemas.history import HistoryAction
from app.schemas.notification import NotificationType
from typing import List, Optional, Dict, Any


class TaskService:
    """Service for task-related business logic"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.task_repo = TaskRepository(db)
        self.project_repo = ProjectRepository(db)
        self.user_repo = UserRepository(db)
        self.history_repo = HistoryRepository(db)
        self.notification_repo = NotificationRepository(db)
    
    async def create_task(self, task_data: TaskCreate, user_id: str) -> dict:
        """Create a new task with automatic history logging and notifications"""
        task_dict = task_data.model_dump()
        
        # Create the task
        task = await self.task_repo.create(task_dict)
        
        # Log creation in history
        history_entry = {
            "task_id": task["_id"],
            "user_id": user_id,
            "action": HistoryAction.CREATED,
            "old_value": None,
            "new_value": task["title"]
        }
        await self.history_repo.create(history_entry)
        
        # Create notification if task is assigned
        if task.get("assigned_to"):
            notification = {
                "user_id": task["assigned_to"],
                "message": f"Nueva tarea asignada: {task['title']}",
                "type": NotificationType.TASK_ASSIGNED
            }
            await self.notification_repo.create(notification)
        
        return task
    
    async def get_all_tasks(self) -> List[dict]:
        """Get all tasks"""
        return await self.task_repo.get_all()
    
    async def get_task(self, task_id: str) -> Optional[dict]:
        """Get a task by ID"""
        return await self.task_repo.find_by_id(task_id)
    
    async def get_tasks_with_details(self) -> List[TaskWithDetails]:
        """Get all tasks with project and user details"""
        tasks = await self.task_repo.get_all()
        projects = await self.project_repo.get_all()
        users = await self.user_repo.get_all()
        
        # Create lookup dictionaries
        project_map = {p["_id"]: p["name"] for p in projects}
        user_map = {u["_id"]: u["username"] for u in users}
        
        # Enrich tasks with details
        enriched_tasks = []
        for task in tasks:
            task["project_name"] = project_map.get(task.get("project_id"))
            task["assigned_to_name"] = user_map.get(task.get("assigned_to"))
            enriched_tasks.append(task)
        
        return enriched_tasks
    
    async def update_task(self, task_id: str, task_data: TaskUpdate, user_id: str) -> bool:
        """Update a task with automatic history logging and notifications"""
        # Get current task
        current_task = await self.task_repo.find_by_id(task_id)
        if not current_task:
            return False
        
        update_dict = task_data.model_dump(exclude_unset=True)
        if not update_dict:
            return False
        
        # Track changes for history
        changes = []
        
        # Check for status change
        if "status" in update_dict and update_dict["status"] != current_task.get("status"):
            changes.append({
                "action": HistoryAction.STATUS_CHANGED,
                "old_value": current_task.get("status"),
                "new_value": update_dict["status"]
            })
        
        # Check for title change
        if "title" in update_dict and update_dict["title"] != current_task.get("title"):
            changes.append({
                "action": HistoryAction.TITLE_CHANGED,
                "old_value": current_task.get("title"),
                "new_value": update_dict["title"]
            })
        
        # Check for priority change
        if "priority" in update_dict and update_dict["priority"] != current_task.get("priority"):
            changes.append({
                "action": HistoryAction.PRIORITY_CHANGED,
                "old_value": current_task.get("priority"),
                "new_value": update_dict["priority"]
            })
        
        # Check for assignment change
        if "assigned_to" in update_dict and update_dict["assigned_to"] != current_task.get("assigned_to"):
            changes.append({
                "action": HistoryAction.ASSIGNED,
                "old_value": current_task.get("assigned_to"),
                "new_value": update_dict["assigned_to"]
            })
            
            # Create notification for new assignee
            if update_dict["assigned_to"]:
                notification = {
                    "user_id": update_dict["assigned_to"],
                    "message": f"Tarea actualizada y asignada a ti: {current_task['title']}",
                    "type": NotificationType.TASK_UPDATED
                }
                await self.notification_repo.create(notification)
        
        # If no specific changes, log as general update
        if not changes:
            changes.append({
                "action": HistoryAction.UPDATED,
                "old_value": None,
                "new_value": None
            })
        
        # Log all changes in history
        for change in changes:
            history_entry = {
                "task_id": task_id,
                "user_id": user_id,
                "action": change["action"],
                "old_value": change.get("old_value"),
                "new_value": change.get("new_value")
            }
            await self.history_repo.create(history_entry)
        
        # Update the task
        return await self.task_repo.update(task_id, update_dict)
    
    async def delete_task(self, task_id: str, user_id: str) -> bool:
        """Delete a task with history logging"""
        # Get current task for history
        task = await self.task_repo.find_by_id(task_id)
        if not task:
            return False
        
        # Log deletion
        history_entry = {
            "task_id": task_id,
            "user_id": user_id,
            "action": HistoryAction.DELETED,
            "old_value": task["title"],
            "new_value": None
        }
        await self.history_repo.create(history_entry)
        
        # Delete the task
        result = await self.task_repo.delete(task_id)
        
        # Optionally delete task history after some time
        # For now we keep it for audit purposes
        
        return result
    
    async def search_tasks(self, filters: Dict[str, Any]) -> List[dict]:
        """Search tasks with filters"""
        return await self.task_repo.search(filters)

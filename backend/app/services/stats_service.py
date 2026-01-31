from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.user_repository import UserRepository
from datetime import datetime
from typing import Dict, Any, List
from collections import defaultdict


class StatsService:
    """Service for statistics and metrics"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.task_repo = TaskRepository(db)
        self.project_repo = ProjectRepository(db)
        self.user_repo = UserRepository(db)
    
    async def get_task_statistics(self) -> Dict[str, Any]:
        """Get comprehensive task statistics"""
        tasks = await self.task_repo.get_all()
        
        total_tasks = len(tasks)
        completed_tasks = sum(1 for t in tasks if t.get("status") == "Completada")
        pending_tasks = sum(1 for t in tasks if t.get("status") == "Pendiente")
        in_progress_tasks = sum(1 for t in tasks if t.get("status") == "En Progreso")
        
        # High priority and critical tasks
        high_priority = sum(1 for t in tasks if t.get("priority") in ["Alta", "Crítica"])
        
        # Overdue tasks
        now = datetime.utcnow()
        overdue_tasks = sum(
            1 for t in tasks 
            if t.get("due_date") and t["due_date"] < now and t.get("status") != "Completada"
        )
        
        return {
            "total": total_tasks,
            "completed": completed_tasks,
            "pending": pending_tasks,
            "in_progress": in_progress_tasks,
            "high_priority": high_priority,
            "overdue": overdue_tasks
        }
    
    async def get_tasks_by_status(self) -> Dict[str, int]:
        """Get task count grouped by status"""
        tasks = await self.task_repo.get_all()
        status_count = defaultdict(int)
        
        for task in tasks:
            status = task.get("status", "Unknown")
            status_count[status] += 1
        
        return dict(status_count)
    
    async def get_tasks_by_project(self) -> List[Dict[str, Any]]:
        """Get task count grouped by project"""
        tasks = await self.task_repo.get_all()
        projects = await self.project_repo.get_all()
        
        project_map = {p["_id"]: p["name"] for p in projects}
        project_count = defaultdict(int)
        
        for task in tasks:
            project_id = task.get("project_id")
            if project_id:
                project_name = project_map.get(project_id, "Unknown")
                project_count[project_name] += 1
        
        return [
            {"project": name, "count": count}
            for name, count in project_count.items()
        ]
    
    async def get_tasks_by_user(self) -> List[Dict[str, Any]]:
        """Get task count grouped by assigned user"""
        tasks = await self.task_repo.get_all()
        users = await self.user_repo.get_all()
        
        user_map = {u["_id"]: u["username"] for u in users}
        user_count = defaultdict(int)
        
        for task in tasks:
            user_id = task.get("assigned_to")
            if user_id:
                username = user_map.get(user_id, "Unknown")
                user_count[username] += 1
        
        return [
            {"user": name, "count": count}
            for name, count in user_count.items()
        ]

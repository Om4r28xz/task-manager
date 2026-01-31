from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDIENTE = "Pendiente"
    EN_PROGRESO = "En Progreso"
    COMPLETADA = "Completada"


class TaskPriority(str, Enum):
    """Task priority enumeration"""
    BAJA = "Baja"
    MEDIA = "Media"
    ALTA = "Alta"
    CRITICA = "Crítica"


class TaskBase(BaseModel):
    """Base task schema"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDIENTE
    priority: TaskPriority = TaskPriority.MEDIA
    project_id: Optional[str] = None
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None
    estimated_hours: Optional[float] = None


class TaskCreate(TaskBase):
    """Schema for creating a task"""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    project_id: Optional[str] = None
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None
    estimated_hours: Optional[float] = None


class Task(TaskBase):
    """Task schema for API responses"""
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True


class TaskWithDetails(Task):
    """Task schema with joined details (project name, user name)"""
    project_name: Optional[str] = None
    assigned_to_name: Optional[str] = None

"""
Database Initialization Script

This script initializes the MongoDB database with:
- Collections and indexes
- Default users (admin, user1, user2)
- Sample projects
- Sample tasks

Run this script to set up or reset the database:
python scripts/init_db.py
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.append(str(Path(__file__).parent.parent))

from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.utils.security import get_password_hash
from datetime import datetime, timedelta


async def init_database():
    """Initialize the database with collections, indexes, and sample data"""
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    
    print(f"Initializing database: {settings.MONGODB_DB_NAME}")
    
    # Drop existing collections (optional - comment out to preserve data)
    print("Dropping existing collections...")
    await db.users.drop()
    await db.projects.drop()
    await db.tasks.drop()
    await db.comments.drop()
    await db.notifications.drop()
    await db.history.drop()
    
    # Create indexes
    print("Creating indexes...")
    
    # Users indexes
    await db.users.create_index("username", unique=True)
    await db.users.create_index("email", unique=True)
    
    # Projects indexes
    await db.projects.create_index("name")
    await db.projects.create_index("created_by")
    
    # Tasks indexes
    await db.tasks.create_index("status")
    await db.tasks.create_index("priority")
    await db.tasks.create_index("project_id")
    await db.tasks.create_index("assigned_to")
    await db.tasks.create_index("due_date")
    await db.tasks.create_index("created_at")
    
    # Comments indexes
    await db.comments.create_index("task_id")
    await db.comments.create_index("created_at")
    
    # Notifications indexes
    await db.notifications.create_index("user_id")
    await db.notifications.create_index("read")
    await db.notifications.create_index("created_at")
    
    # History indexes
    await db.history.create_index("task_id")
    await db.history.create_index("timestamp")
    await db.history.create_index([("task_id", 1), ("timestamp", -1)])
    
    print("Indexes created successfully")
    
    # Create default users
    print("Creating default users...")
    
    users = [
        {
            "username": "admin",
            "email": "admin@taskmanager.com",
            "hashed_password": get_password_hash("admin123"),
            "created_at": datetime.utcnow()
        },
        {
            "username": "user1",
            "email": "user1@taskmanager.com",
            "hashed_password": get_password_hash("user123"),
            "created_at": datetime.utcnow()
        },
        {
            "username": "user2",
            "email": "user2@taskmanager.com",
            "hashed_password": get_password_hash("user123"),
            "created_at": datetime.utcnow()
        }
    ]
    
    result = await db.users.insert_many(users)
    user_ids = [str(id) for id in result.inserted_ids]
    print(f"Created {len(users)} users")
    
    # Create sample projects
    print("Creating sample projects...")
    
    projects = [
        {
            "name": "Proyecto Alpha",
            "description": "Desarrollo de nuevo sistema de gestión",
            "created_by": user_ids[0],
            "created_at": datetime.utcnow()
        },
        {
            "name": "Proyecto Beta",
            "description": "Implementación de API REST",
            "created_by": user_ids[0],
            "created_at": datetime.utcnow()
        },
        {
            "name": "Proyecto Demo",
            "description": "Proyecto de demostración",
            "created_by": user_ids[1],
            "created_at": datetime.utcnow()
        }
    ]
    
    result = await db.projects.insert_many(projects)
    project_ids = [str(id) for id in result.inserted_ids]
    print(f"Created {len(projects)} projects")
    
    # Create sample tasks
    print("Creating sample tasks...")
    
    now = datetime.utcnow()
    
    tasks = [
        {
            "title": "Diseñar base de datos",
            "description": "Crear el modelo de datos para el sistema",
            "status": "Completada",
            "priority": "Alta",
            "project_id": project_ids[0],
            "assigned_to": user_ids[1],
            "due_date": now - timedelta(days=5),
            "estimated_hours": 8.0,
            "created_at": now - timedelta(days=10),
            "updated_at": now - timedelta(days=5)
        },
        {
            "title": "Implementar API de autenticación",
            "description": "Desarrollar endpoints de login y registro",
            "status": "En Progreso",
            "priority": "Alta",
            "project_id": project_ids[0],
            "assigned_to": user_ids[2],
            "due_date": now + timedelta(days=3),
            "estimated_hours": 12.0,
            "created_at": now - timedelta(days=7),
            "updated_at": now - timedelta(days=1)
        },
        {
            "title": "Crear documentación técnica",
            "description": "Documentar la arquitectura del sistema",
            "status": "Pendiente",
            "priority": "Media",
            "project_id": project_ids[0],
            "assigned_to": user_ids[1],
            "due_date": now + timedelta(days=7),
            "estimated_hours": 6.0,
            "created_at": now - timedelta(days=5),
            "updated_at": now - timedelta(days=5)
        },
        {
            "title": "Desarrollar endpoints REST",
            "description": "Implementar CRUD completo para todas las entidades",
            "status": "En Progreso",
            "priority": "Crítica",
            "project_id": project_ids[1],
            "assigned_to": user_ids[2],
            "due_date": now + timedelta(days=2),
            "estimated_hours": 20.0,
            "created_at": now - timedelta(days=6),
            "updated_at": now
        },
        {
            "title": "Pruebas de integración",
            "description": "Realizar pruebas end-to-end del sistema",
            "status": "Pendiente",
            "priority": "Alta",
            "project_id": project_ids[1],
            "assigned_to": user_ids[1],
            "due_date": now + timedelta(days=10),
            "estimated_hours": 16.0,
            "created_at": now - timedelta(days=3),
            "updated_at": now - timedelta(days=3)
        },
        {
            "title": "Tarea de ejemplo",
            "description": "Esta es una tarea de demostración",
            "status": "Pendiente",
            "priority": "Baja",
            "project_id": project_ids[2],
            "assigned_to": user_ids[0],
            "due_date": now + timedelta(days=14),
            "estimated_hours": 4.0,
            "created_at": now - timedelta(days=2),
            "updated_at": now - timedelta(days=2)
        }
    ]
    
    result = await db.tasks.insert_many(tasks)
    task_ids = [str(id) for id in result.inserted_ids]
    print(f"Created {len(tasks)} tasks")
    
    # Create sample comments
    print("Creating sample comments...")
    
    comments = [
        {
            "task_id": task_ids[0],
            "user_id": user_ids[0],
            "content": "Excelente trabajo en el diseño de la base de datos",
            "created_at": now - timedelta(days=4)
        },
        {
            "task_id": task_ids[1],
            "user_id": user_ids[1],
            "content": "Estoy trabajando en la integración con JWT",
            "created_at": now - timedelta(days=1)
        },
        {
            "task_id": task_ids[3],
            "user_id": user_ids[2],
            "content": "Ya implementé los endpoints de usuarios y proyectos",
            "created_at": now - timedelta(hours=5)
        }
    ]
    
    await db.comments.insert_many(comments)
    print(f"Created {len(comments)} comments")
    
    # Create sample history entries
    print("Creating sample history entries...")
    
    history = [
        {
            "task_id": task_ids[0],
            "user_id": user_ids[0],
            "action": "CREATED",
            "old_value": None,
            "new_value": "Diseñar base de datos",
            "timestamp": now - timedelta(days=10)
        },
        {
            "task_id": task_ids[0],
            "user_id": user_ids[0],
            "action": "STATUS_CHANGED",
            "old_value": "Pendiente",
            "new_value": "Completada",
            "timestamp": now - timedelta(days=5)
        },
        {
            "task_id": task_ids[1],
            "user_id": user_ids[0],
            "action": "CREATED",
            "old_value": None,
            "new_value": "Implementar API de autenticación",
            "timestamp": now - timedelta(days=7)
        },
        {
            "task_id": task_ids[1],
            "user_id": user_ids[2],
            "action": "STATUS_CHANGED",
            "old_value": "Pendiente",
            "new_value": "En Progreso",
            "timestamp": now - timedelta(days=1)
        }
    ]
    
    await db.history.insert_many(history)
    print(f"Created {len(history)} history entries")
    
    # Create sample notifications
    print("Creating sample notifications...")
    
    notifications = [
        {
            "user_id": user_ids[1],
            "message": "Nueva tarea asignada: Diseñar base de datos",
            "type": "task_assigned",
            "read": True,
            "created_at": now - timedelta(days=10)
        },
        {
            "user_id": user_ids[2],
            "message": "Nueva tarea asignada: Implementar API de autenticación",
            "type": "task_assigned",
            "read": True,
            "created_at": now - timedelta(days=7)
        },
        {
            "user_id": user_ids[2],
            "message": "Nueva tarea asignada: Desarrollar endpoints REST",
            "type": "task_assigned",
            "read": False,
            "created_at": now - timedelta(days=6)
        },
        {
            "user_id": user_ids[1],
            "message": "Nueva tarea asignada: Pruebas de integración",
            "type": "task_assigned",
            "read": False,
            "created_at": now - timedelta(days=3)
        }
    ]
    
    await db.notifications.insert_many(notifications)
    print(f"Created {len(notifications)} notifications")
    
    print("\n" + "="*50)
    print("DATABASE INITIALIZATION COMPLETE!")
    print("="*50)
    print(f"\nDefault Users Created:")
    print(f"  Username: admin    | Password: admin123")
    print(f"  Username: user1    | Password: user123")
    print(f"  Username: user2    | Password: user123")
    print(f"\nDatabase: {settings.MONGODB_DB_NAME}")
    print(f"Projects: {len(projects)}")
    print(f"Tasks: {len(tasks)}")
    print(f"Comments: {len(comments)}")
    print(f"Notifications: {len(notifications)}")
    print(f"History Entries: {len(history)}")
    print("\nYou can now start the server with: uvicorn app.main:app --reload")
    
    # Close connection
    client.close()


if __name__ == "__main__":
    asyncio.run(init_database())

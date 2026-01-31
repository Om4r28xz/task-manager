# Database Schema Documentation

## Overview

This document describes the MongoDB database schema for the Task Manager application. The database uses MongoDB's flexible document model to store all application data with proper relationships and indexes for optimal performance.

## Collections

### 1. Users (`users`)

Stores user accounts and authentication information.

**Fields:**
- `_id`: ObjectId - Unique identifier (auto-generated)
- `username`: String (required, unique) - User's login name
- `email`: String (required, unique) - User's email address
- `hashed_password`: String (required) - Bcrypt hashed password
- `created_at`: DateTime (required) - Account creation timestamp

**Indexes:**
- `username` (unique)
- `email` (unique)

**Example Document:**
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "username": "admin",
  "email": "admin@taskmanager.com",
  "hashed_password": "$2b$12$...",
  "created_at": "2026-01-25T10:00:00.000Z"
}
```

---

### 2. Projects (`projects`)

Stores project information.

**Fields:**
- `_id`: ObjectId - Unique identifier
- `name`: String (required) - Project name
- `description`: String (optional) - Project description
- `created_by`: String (required) - Reference to User `_id`
- `created_at`: DateTime (required) - Project creation timestamp

**Indexes:**
- `name`
- `created_by`

**Relationships:**
- `created_by` → `users._id` (many-to-one)

**Example Document:**
```json
{
  "_id": "507f1f77bcf86cd799439012",
  "name": "Proyecto Alpha",
  "description": "Desarrollo de nuevo sistema de gestión",
  "created_by": "507f1f77bcf86cd799439011",
  "created_at": "2026-01-25T10:00:00.000Z"
}
```

---

### 3. Tasks (`tasks`)

Stores all task information.

**Fields:**
- `_id`: ObjectId - Unique identifier
- `title`: String (required) - Task title
- `description`: String (optional) - Detailed description
- `status`: String (required) - One of: "Pendiente", "En Progreso", "Completada"
- `priority`: String (required) - One of: "Baja", "Media", "Alta", "Crítica"
- `project_id`: String (optional) - Reference to Project `_id`
- `assigned_to`: String (optional) - Reference to User `_id`
- `due_date`: DateTime (optional) - Task deadline
- `estimated_hours`: Float (optional) - Estimated hours for completion
- `created_at`: DateTime (required) - Task creation timestamp
- `updated_at`: DateTime (required) - Last update timestamp

**Indexes:**
- `status`
- `priority`
- `project_id`
- `assigned_to`
- `due_date`
- `created_at`

**Relationships:**
- `project_id` → `projects._id` (many-to-one)
- `assigned_to` → `users._id` (many-to-one)

**Example Document:**
```json
{
  "_id": "507f1f77bcf86cd799439013",
  "title": "Diseñar base de datos",
  "description": "Crear el modelo de datos para el sistema",
  "status": "Completada",
  "priority": "Alta",
  "project_id": "507f1f77bcf86cd799439012",
  "assigned_to": "507f1f77bcf86cd799439011",
  "due_date": "2026-01-30T23:59:59.000Z",
  "estimated_hours": 8.0,
  "created_at": "2026-01-15T10:00:00.000Z",
  "updated_at": "2026-01-20T15:30:00.000Z"
}
```

---

### 4. Comments (`comments`)

Stores comments on tasks.

**Fields:**
- `_id`: ObjectId - Unique identifier
- `task_id`: String (required) - Reference to Task `_id`
- `user_id`: String (required) - Reference to User `_id`
- `content`: String (required) - Comment text
- `created_at`: DateTime (required) - Comment timestamp

**Indexes:**
- `task_id`
- `created_at`

**Relationships:**
- `task_id` → `tasks._id` (many-to-one)
- `user_id` → `users._id` (many-to-one)

**Example Document:**
```json
{
  "_id": "507f1f77bcf86cd799439014",
  "task_id": "507f1f77bcf86cd799439013",
  "user_id": "507f1f77bcf86cd799439011",
  "content": "Excelente trabajo en el diseño",
  "created_at": "2026-01-21T10:00:00.000Z"
}
```

---

### 5. Notifications (`notifications`)

Stores user notifications.

**Fields:**
- `_id`: ObjectId - Unique identifier
- `user_id`: String (required) - Reference to User `_id`
- `message`: String (required) - Notification message
- `type`: String (required) - One of: "task_assigned", "task_updated", "task_completed", "comment_added"
- `read`: Boolean (default: false) - Read status
- `created_at`: DateTime (required) - Notification timestamp

**Indexes:**
- `user_id`
- `read`
- `created_at`

**Relationships:**
- `user_id` → `users._id` (many-to-one)

**Example Document:**
```json
{
  "_id": "507f1f77bcf86cd799439015",
  "user_id": "507f1f77bcf86cd799439011",
  "message": "Nueva tarea asignada: Diseñar base de datos",
  "type": "task_assigned",
  "read": false,
  "created_at": "2026-01-15T10:00:00.000Z"
}
```

---

### 6. History (`history`)

Audit log for task changes.

**Fields:**
- `_id`: ObjectId - Unique identifier
- `task_id`: String (required) - Reference to Task `_id`
- `user_id`: String (required) - Reference to User `_id`
- `action`: String (required) - One of: "CREATED", "STATUS_CHANGED", "TITLE_CHANGED", "ASSIGNED", "PRIORITY_CHANGED", "UPDATED", "DELETED"
- `old_value`: String (optional) - Previous value
- `new_value`: String (optional) - New value
- `timestamp`: DateTime (required) - Change timestamp

**Indexes:**
- `task_id`
- `timestamp`
- Compound: (`task_id`, `timestamp`) descending

**Relationships:**
- `task_id` → `tasks._id` (many-to-one)
- `user_id` → `users._id` (many-to-one)

**Example Document:**
```json
{
  "_id": "507f1f77bcf86cd799439016",
  "task_id": "507f1f77bcf86cd799439013",
  "user_id": "507f1f77bcf86cd799439011",
  "action": "STATUS_CHANGED",
  "old_value": "Pendiente",
  "new_value": "Completada",
  "timestamp": "2026-01-20T15:30:00.000Z"
}
```

---

## Relationships Diagram

```
users (1) ──< created_by ──< (N) projects
users (1) ──< assigned_to ──< (N) tasks
projects (1) ──< project_id ──< (N) tasks
tasks (1) ──< task_id ──< (N) comments
tasks (1) ──< task_id ──< (N) history
users (1) ──< user_id ──< (N) notifications
users (1) ──< user_id ──< (N) comments
users (1) ──< user_id ──< (N) history
```

## Data Integrity Notes

1. **Referential Integrity**: While MongoDB doesn't enforce foreign key constraints, the application layer ensures data integrity through the repository and service layers.

2. **Cascading Deletes**: The application handles cascading operations:
   - Deleting a task creates a history entry before deletion
   - Task history can be preserved even after task deletion for audit purposes

3. **Timestamps**: All collections include timestamp fields (`created_at`, `updated_at`, or `timestamp`) for audit trails.

4. **Indexes**: All foreign key fields and frequently queried fields are indexed for optimal performance.

5. **String IDs**: ObjectIds are converted to strings in the application layer for consistent handling across the API.

# Task Manager - Setup Instructions

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **MongoDB 6.0+** - [Download MongoDB](https://www.mongodb.com/try/download/community)

## Project Structure

```
C:\Users\omar2\Documents\Escuelazzz\SEVENTH TETRA\SW ARCHITECTURE\task-manager/
├── backend/          # FastAPI Backend
├── frontend/         # React Frontend
└── docs/            # Documentation
```

## Backend Setup

### 1. Navigate to Backend Directory

```bash
cd "C:\Users\omar2\Documents\Escuelazzz\SEVENTH TETRA\SW ARCHITECTURE\task-manager\backend"
```

### 2. Create Virtual Environment (Optional but Recommended)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file in the backend directory:

```bash
copy .env.example .env
```

Edit `.env` with your configuration:

```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=task_manager

# JWT Configuration (CHANGE IN PRODUCTION!)
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Application Configuration
APP_NAME=Task Manager API
APP_VERSION=1.0.0
```

### 5. Start MongoDB

Make sure MongoDB is running on your system:

```bash
# If MongoDB is installed as a service, it should start automatically
# Otherwise, start it manually:
mongod
```

### 6. Initialize Database

Run the initialization script to create collections, indexes, and sample data:

```bash
python scripts\init_db.py
```

**Default Users Created:**
- **Username**: `admin` | **Password**: `admin123`
- **Username**: `user1` | **Password**: `user123`
- **Username**: `user2` | **Password**: `user123`

### 7. Start the Backend Server

```bash
uvicorn app.main:app --reload
```

The API will be available at: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs**

---

## Frontend Setup

### 1. Navigate to Frontend Directory

```bash
cd "C:\Users\omar2\Documents\Escuelazzz\SEVENTH TETRA\SW ARCHITECTURE\task-manager\frontend"
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Start Development Server

```bash
npm run dev
```

The application will be available at: **http://localhost:5173**

---

## Running the Complete Application

### Option 1: Two Terminals

**Terminal 1 - Backend:**
```bash
cd "C:\Users\omar2\Documents\Escuelazzz\SEVENTH TETRA\SW ARCHITECTURE\task-manager\backend"
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd "C:\Users\omar2\Documents\Escuelazzz\SEVENTH TETRA\SW ARCHITECTURE\task-manager\frontend"
npm run dev
```

### Option 2: Using PowerShell Job (Background Process)

```powershell
# Start backend in background
cd "C:\Users\omar2\Documents\Escuelazzz\SEVENTH TETRA\SW ARCHITECTURE\task-manager\backend"
Start-Job -ScriptBlock { uvicorn app.main:app --reload }

# Start frontend
cd "C:\Users\omar2\Documents\Escuelazzz\SEVENTH TETRA\SW ARCHITECTURE\task-manager\frontend"
npm run dev
```

---

## Accessing the Application

1. **Open your browser** and navigate to: **http://localhost:5173**

2. **Login** with one of the default users:
   - `admin` / `admin123`
   - `user1` / `user123`
   - `user2` / `user123`

3. **Explore the features**:
   - Create and manage tasks
   - Create projects
   - View real-time statistics
   - Search and filter tasks
   - View notifications
   - Check audit history
   - Generate reports

---

## Database Management

### View Database Contents

Using MongoDB Compass (GUI):
1. Download and install [MongoDB Compass](https://www.mongodb.com/try/download/compass)
2. Connect to: `mongodb://localhost:27017`
3. Select database: `task_manager`

Using MongoDB Shell:
```bash
mongosh
use task_manager
db.tasks.find().pretty()
db.users.find().pretty()
```

### Reset Database

To reset the database with fresh sample data:

```bash
cd "C:\Users\omar2\Documents\Escuelazzz\SEVENTH TETRA\SW ARCHITECTURE\task-manager\backend"
python scripts\init_db.py
```

**Warning**: This will delete all existing data!

---

## Production Build

### Backend

For production deployment:

1. Update `.env` with production settings
2. Use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend

Build the production bundle:

```bash
cd "C:\Users\omar2\Documents\Escuelazzz\SEVENTH TETRA\SW ARCHITECTURE\task-manager\frontend"
npm run build
```

The optimized files will be in the `dist/` directory.

---

## Troubleshooting

### Backend Issues

**Error: "Module not found"**
- Ensure you're in the correct directory
- Try reinstalling dependencies: `pip install -r requirements.txt`

**Error: "MongoDB connection failed"**
- Verify MongoDB is running: `mongosh`
- Check the connection string in `.env`

**Error: "Port 8000 already in use"**
- Stop other processes using port 8000
- Or change the port: `uvicorn app.main:app --port 8001`

### Frontend Issues

**Error: "Cannot find module"**
- Delete `node_modules` and reinstall: `rm -r node_modules && npm install`

**Error: "Network error" when calling API**
- Ensure the backend is running on port 8000
- Check the proxy configuration in `vite.config.js`

**Error: "Port 5173 already in use"**
- Use a different port: `npm run dev -- --port 3000`

### Database Issues

**Cannot connect to MongoDB**
- Ensure MongoDB service is running
- Check Windows Services for "MongoDB"
- Try starting manually: `mongod --dbpath C:\data\db`

---

## Architecture Overview

This application uses a **layered architecture**:

### Backend (FastAPI)
1. **API Layer** (`routers/`) - HTTP endpoints
2. **Service Layer** (`services/`) - Business logic
3. **Repository Layer** (`repositories/`) - Data access
4. **Models** (`schemas/`) - Data validation

### Frontend (React)
- **Components** - Reusable UI elements
- **Services** - API communication
- **State Management** - React hooks

### Database (MongoDB)
- Document-based NoSQL database
- Collections: users, projects, tasks, comments, notifications, history

---

## Features

✅ **Authentication** - JWT-based secure login  
✅ **Task Management** - Full CRUD with status tracking  
✅ **Project Organization** - Group tasks by projects  
✅ **Real-time Statistics** - Dashboard with metrics  
✅ **Audit Log** - Complete history of changes  
✅ **Notifications** - User alerts for task assignments  
✅ **Search & Filter** - Advanced task filtering  
✅ **Export** - DataTables integration for PDF/CSV/Excel export  
✅ **Responsive Design** - Futuristic glassmorphism UI  

---

## Support

For issues or questions:
1. Check the API documentation at http://localhost:8000/docs
2. Review the database schema in `docs/DATABASE_SCHEMA.md`
3. Verify all services are running correctly

---

## License

This project is created for educational purposes as part of the Software Architecture course.

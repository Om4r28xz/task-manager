from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import connect_to_mongo, close_mongo_connection
from app.routers import auth, tasks, projects, comments, notifications, history, reports

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Task Manager API with layered architecture"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Event handlers
@app.on_event("startup")
async def startup_event():
    """Connect to database on startup"""
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    await close_mongo_connection()


# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(projects.router)
app.include_router(comments.router)
app.include_router(notifications.router)
app.include_router(history.router)
app.include_router(reports.router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Task Manager API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

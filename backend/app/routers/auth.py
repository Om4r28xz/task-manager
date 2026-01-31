from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import get_database
from app.services.auth_service import AuthService
from app.schemas.user import User, UserCreate
from app.utils.security import decode_access_token
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Optional

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> dict:
    """Dependency to get current authenticated user"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    auth_service = AuthService(db)
    user = await auth_service.get_current_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Login endpoint - returns access token"""
    auth_service = AuthService(db)
    
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = await auth_service.create_token(user)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["_id"],
            "username": user["username"],
            "email": user["email"]
        }
    }


@router.post("/register", response_model=User)
async def register(
    user_data: UserCreate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Register a new user"""
    auth_service = AuthService(db)
    
    try:
        user = await auth_service.register_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/me", response_model=User)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return current_user

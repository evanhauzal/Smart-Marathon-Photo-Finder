"""
Authentication API routes.
Handles user registration, login, and profile retrieval.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from DATABASE_LOGIN.auth import register_user, login_user, get_user_by_id
from BACKEND.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
async def register(request: RegisterRequest):
    """Register a new user (USER or PHOTOGRAPHER)."""
    try:
        user = register_user(
            name=request.name,
            email=request.email,
            password=request.password,
            role=request.role,
        )
        # Convert datetime to string for JSON serialization
        if user.get("created_at"):
            user["created_at"] = str(user["created_at"])
        return {"message": "Registration successful", "user": user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(request: LoginRequest):
    """Login and receive a JWT token."""
    try:
        result = login_user(email=request.email, password=request.password)
        return result
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me")
async def get_profile(user: dict = Depends(get_current_user)):
    """Get the current authenticated user's profile."""
    try:
        user_info = get_user_by_id(user["user_id"])
        if user_info.get("created_at"):
            user_info["created_at"] = str(user_info["created_at"])
        return {"user": user_info}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

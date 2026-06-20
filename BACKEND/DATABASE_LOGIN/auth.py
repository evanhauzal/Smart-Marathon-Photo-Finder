"""
Authentication module.
Handles user registration, login, and JWT token management using Supabase.
"""

import bcrypt
import jwt
import datetime
from .db import get_supabase_client

# JWT Configuration
JWT_SECRET = "smart-marathon-secret-key-2026"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(
        password.encode("utf-8"), password_hash.encode("utf-8")
    )


def generate_token(user_id: int, email: str, role: str) -> str:
    """Generate a JWT token for authenticated user."""
    payload = {
        "user_id": user_id,
        "email": email,
        "role": role,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": datetime.datetime.utcnow(),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")


def register_user(name: str, email: str, password: str, role: str) -> dict:
    """
    Register a new user using Supabase Client.
    Returns user info dict on success.
    Raises ValueError on duplicate email or invalid role.
    """
    if role not in ("USER", "PHOTOGRAPHER"):
        raise ValueError("Role must be 'USER' or 'PHOTOGRAPHER'")

    password_hashed = hash_password(password)
    supabase = get_supabase_client()

    try:
        response = supabase.table("users").insert({
            "name": name,
            "email": email,
            "password_hash": password_hashed,
            "role": role
        }).execute()

        if not response.data:
            raise ValueError("Failed to register user")

        return response.data[0]
        
    except Exception as e:
        if "duplicate key" in str(e).lower() or "already registered" in str(e).lower():
            raise ValueError("Email already registered")
        raise


def login_user(email: str, password: str) -> dict:
    """
    Authenticate a user using Supabase Client and return a JWT token.
    Returns dict with token and user info.
    Raises ValueError on invalid credentials.
    """
    supabase = get_supabase_client()

    response = supabase.table("users").select("*").eq("email", email).execute()
    
    if not response.data:
        raise ValueError("Invalid email or password")
        
    user = response.data[0]

    if not verify_password(password, user["password_hash"]):
        raise ValueError("Invalid email or password")

    token = generate_token(user["id"], user["email"], user["role"])

    return {
        "token": token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
        },
    }


def get_user_by_id(user_id: int) -> dict:
    """Fetch user info by ID using Supabase Client."""
    supabase = get_supabase_client()

    response = supabase.table("users").select("id, name, email, role, created_at").eq("id", user_id).execute()
    
    if not response.data:
        raise ValueError("User not found")
        
    return response.data[0]
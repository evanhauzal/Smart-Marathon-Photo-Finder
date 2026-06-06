"""
Authentication module.
Handles user registration, login, and JWT token management.
"""

import bcrypt
import jwt
import datetime
from .db import get_connection

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
    Register a new user.
    Returns user info dict on success.
    Raises ValueError on duplicate email or invalid role.
    """
    if role not in ("USER", "PHOTOGRAPHER"):
        raise ValueError("Role must be 'USER' or 'PHOTOGRAPHER'")

    password_hashed = hash_password(password)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (name, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
            RETURNING id, name, email, role, created_at
            """,
            (name, email, password_hashed, role),
        )
        user = cursor.fetchone()
        conn.commit()
        return dict(user)
    except Exception as e:
        conn.rollback()
        if "unique" in str(e).lower():
            raise ValueError("Email already registered")
        raise
    finally:
        cursor.close()
        conn.close()


def login_user(email: str, password: str) -> dict:
    """
    Authenticate a user and return a JWT token.
    Returns dict with token and user info.
    Raises ValueError on invalid credentials.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id, name, email, password_hash, role FROM users WHERE email = %s",
            (email,),
        )
        user = cursor.fetchone()

        if not user:
            raise ValueError("Invalid email or password")

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
    finally:
        cursor.close()
        conn.close()


def get_user_by_id(user_id: int) -> dict:
    """Fetch user info by ID."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id, name, email, role, created_at FROM users WHERE id = %s",
            (user_id,),
        )
        user = cursor.fetchone()
        if not user:
            raise ValueError("User not found")
        return dict(user)
    finally:
        cursor.close()
        conn.close()

"""
JWT authentication middleware for FastAPI.
Provides dependency injection for route protection and role-based access control.
"""

from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from DATABASE_LOGIN.auth import decode_token

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    Dependency that extracts and validates the JWT token.
    Returns the decoded user payload.
    """
    try:
        payload = decode_token(credentials.credentials)
        return payload
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


def require_role(required_role: str):
    """
    Dependency factory that checks if the user has the required role.

    Usage:
        @router.get("/protected")
        async def protected(user=Depends(require_role("PHOTOGRAPHER"))):
            ...
    """

    async def role_checker(
        credentials: HTTPAuthorizationCredentials = Depends(security),
    ) -> dict:
        try:
            payload = decode_token(credentials.credentials)
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))

        if payload.get("role") != required_role:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. Required role: {required_role}",
            )

        return payload

    return role_checker

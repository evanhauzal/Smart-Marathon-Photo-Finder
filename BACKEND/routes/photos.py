"""
Photo management API routes.
Handles event photo uploads and listing for photographers.
"""

import os
import uuid
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.responses import FileResponse
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from BACKEND.middleware.auth_middleware import require_role, get_current_user

router = APIRouter(prefix="/api/photos", tags=["Photos"])

# Base directory for photos
PHOTOS_BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "PHOTOS")


@router.post("/upload")
async def upload_photos(
    event_name: str = Form(...),
    files: list[UploadFile] = File(...),
    user: dict = Depends(require_role("PHOTOGRAPHER")),
):
    """
    Upload event photos. Only accessible by PHOTOGRAPHER role.
    Photos are saved to PHOTOS/{event_name}/ directory.
    """
    # Sanitize event name (replace spaces with underscores, remove special chars)
    safe_event_name = "".join(
        c if c.isalnum() or c in ("_", "-") else "_" for c in event_name
    )

    event_dir = os.path.join(PHOTOS_BASE_DIR, safe_event_name)
    os.makedirs(event_dir, exist_ok=True)

    uploaded_files = []
    supported_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

    for file in files:
        # Validate file extension
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in supported_extensions:
            continue

        # Generate unique filename to avoid collisions
        unique_name = f"{uuid.uuid4().hex}{ext}"
        file_path = os.path.join(event_dir, unique_name)

        # Save file
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        uploaded_files.append(
            {
                "original_name": file.filename,
                "saved_name": unique_name,
                "event_name": safe_event_name,
            }
        )

    if not uploaded_files:
        raise HTTPException(
            status_code=400,
            detail="No valid image files were uploaded",
        )

    return {
        "message": f"{len(uploaded_files)} photo(s) uploaded successfully",
        "files": uploaded_files,
    }


@router.get("/list")
async def list_photos(user: dict = Depends(require_role("PHOTOGRAPHER"))):
    """
    List all uploaded event photos. Only accessible by PHOTOGRAPHER role.
    Returns a dict of events and their photo filenames.
    """
    result = {}
    supported_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

    if not os.path.exists(PHOTOS_BASE_DIR):
        return {"events": result}

    for event_dir_name in sorted(os.listdir(PHOTOS_BASE_DIR)):
        event_dir_path = os.path.join(PHOTOS_BASE_DIR, event_dir_name)
        if not os.path.isdir(event_dir_path):
            continue

        photos = []
        for filename in sorted(os.listdir(event_dir_path)):
            ext = os.path.splitext(filename)[1].lower()
            if ext in supported_extensions:
                photos.append(filename)

        if photos:
            result[event_dir_name] = photos

    return {"events": result}


@router.get("/events")
async def list_events(user: dict = Depends(get_current_user)):
    """List all available event names."""
    events = []

    if not os.path.exists(PHOTOS_BASE_DIR):
        return {"events": events}

    for event_dir_name in sorted(os.listdir(PHOTOS_BASE_DIR)):
        event_dir_path = os.path.join(PHOTOS_BASE_DIR, event_dir_name)
        if os.path.isdir(event_dir_path):
            photo_count = len([
                f for f in os.listdir(event_dir_path)
                if os.path.splitext(f)[1].lower() in {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
            ])
            events.append({"name": event_dir_name, "photo_count": photo_count})

    return {"events": events}


@router.get("/file/{event_name}/{filename}")
async def get_photo(event_name: str, filename: str):
    """Serve a specific photo file."""
    file_path = os.path.join(PHOTOS_BASE_DIR, event_name, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Photo not found")

    return FileResponse(file_path)

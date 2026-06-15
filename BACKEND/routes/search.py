"""
Search API routes.
Handles face search (ArcFace) and bib number search (EasyOCR).
"""

import os
import uuid
import tempfile
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from BACKEND.middleware.auth_middleware import require_role
from MODEL.face_search import search_all_events as face_search_all
from MODEL.bib_search import search_all_events as bib_search_all

router = APIRouter(prefix="/api/search", tags=["Search"])

# Base directory for photos
PHOTOS_BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "PHOTOS")


@router.post("/face")
async def search_by_face(
    selfie: UploadFile = File(...),
    user: dict = Depends(require_role("USER")),
):
    """
    Search for event photos matching a selfie using ArcFace.
    The selfie is saved temporarily and deleted after search.
    Only accessible by USER role.
    """
    # Validate file type
    supported_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    ext = os.path.splitext(selfie.filename)[1].lower()
    if ext not in supported_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image format. Use JPG, PNG, BMP, or WebP.",
        )

    # Save selfie to a temporary file
    temp_dir = tempfile.gettempdir()
    temp_filename = f"selfie_{uuid.uuid4().hex}{ext}"
    temp_path = os.path.join(temp_dir, temp_filename)

    try:
        # Save uploaded selfie
        content = await selfie.read()
        with open(temp_path, "wb") as f:
            f.write(content)

        # Run face search across all events
        matches = face_search_all(temp_path, PHOTOS_BASE_DIR)

        return {
            "message": f"Found {len(matches)} matching photo(s)",
            "matches": matches,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}",
        )
    finally:
        # Always delete the temporary selfie file
        if os.path.exists(temp_path):
            os.remove(temp_path)


@router.post("/bib")
async def search_by_bib(
    bib_number: str = Form(...),
    user: dict = Depends(require_role("USER")),
):
    """
    Search for event photos containing a specific bib number using EasyOCR.
    Only accessible by USER role.
    """
    if not bib_number.strip():
        raise HTTPException(
            status_code=400, detail="Bib number cannot be empty"
        )

    try:
        matches = bib_search_all(bib_number.strip(), PHOTOS_BASE_DIR)

        return {
            "message": f"Found {len(matches)} matching photo(s)",
            "matches": matches,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}",
        )
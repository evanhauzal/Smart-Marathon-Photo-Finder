"""
Smart Marathon Photo Finder — Backend API Server.
FastAPI application entry point.
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, PROJECT_ROOT)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from DATABASE_LOGIN.db import init_db
from BACKEND.routes.auth import router as auth_router
from BACKEND.routes.photos import router as photos_router
from BACKEND.routes.search import router as search_router

app = FastAPI(
    title="Smart Marathon Photo Finder",
    description="Find your marathon photos using face recognition and bib number search",
    version="1.0.0",
)

# CORS middleware — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for serving photos
photos_dir = os.path.join(PROJECT_ROOT, "PHOTOS")
os.makedirs(photos_dir, exist_ok=True)
app.mount("/photos", StaticFiles(directory=photos_dir), name="photos")

# Include API routers
app.include_router(auth_router)
app.include_router(photos_router)
app.include_router(search_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    print("Initializing database...")
    init_db()
    print("Database initialized. Server is ready.")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Smart Marathon Photo Finder API"}

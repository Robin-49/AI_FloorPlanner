"""
Health Check API Router for AI FloorPlanner Backend.
"""

from fastapi import APIRouter
from config.settings import get_settings
from schemas.responses import HealthResponse

# Try to get active sessions count from the in-memory store
try:
    from services.session_manager import _store
    get_active_sessions = lambda: len(_store._sessions)
except ImportError:
    get_active_sessions = lambda: 0

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """System health check endpoint."""
    settings = get_settings()
    return HealthResponse(
        status="ok",
        service=settings.APP_NAME,
        version=settings.APP_VERSION,
        active_sessions=get_active_sessions()
    )

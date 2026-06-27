"""
API Router package init.
"""

from api.chat import router as chat_router
from api.session import router as session_router
from api.validate import router as validate_router
from api.generate import router as generate_router
from api.health import router as health_router

__all__ = [
    "chat_router",
    "session_router",
    "validate_router",
    "generate_router",
    "health_router",
]

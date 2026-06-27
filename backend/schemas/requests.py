"""
API request schemas for AI FloorPlanner Backend.

These define the shape of incoming data from the frontend.
"""

from typing import Optional

from pydantic import BaseModel


class StartSessionRequest(BaseModel):
    """Request to start a new session. Currently no fields required."""
    pass


class ChatMessageRequest(BaseModel):
    """Incoming chat message from the user."""
    session_id: str
    message: str


class ValidateRequest(BaseModel):
    """Request to validate current requirements for a session."""
    session_id: str


class GenerateRequest(BaseModel):
    """Request to generate a floor plan from collected requirements."""
    session_id: str
    format: Optional[str] = "json"  # json | dxf | svg | freecad (future)

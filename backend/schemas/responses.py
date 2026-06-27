"""
API response schemas for AI FloorPlanner Backend.

These define the shape of outgoing data sent to the frontend.
"""

from typing import Optional

from pydantic import BaseModel


class StartSessionResponse(BaseModel):
    """Response after creating a new session."""
    session_id: str
    reply: str
    workflow_stage: str = "conversation"


class ChatMessageResponse(BaseModel):
    """
    Response after processing a chat message.

    This is the primary response contract between backend and frontend.
    The frontend should render its entire state from this response.
    """
    reply: str
    completion_percentage: int = 0
    requirements: dict = {}

    # Workflow context
    workflow_stage: str = "conversation"
    missing_requirements: list[str] = []
    validation_results: list[str] = []
    next_action: Optional[str] = None


class ValidationResponse(BaseModel):
    """Response from the validation endpoint."""
    session_id: str
    is_valid: bool
    issues: list[str] = []
    missing_requirements: list[str] = []


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "ok"
    service: str = "AI FloorPlanner Backend"
    version: str = "2.0.0"
    active_sessions: int = 0

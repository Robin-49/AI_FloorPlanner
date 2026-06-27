"""
Chat-related Pydantic models for AI FloorPlanner Backend.

Pure data models only — no route handlers or business logic.
"""

from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    """Incoming chat message from the frontend."""
    session_id: str
    message: str


class ChatResponse(BaseModel):
    """
    Response sent back to the frontend after processing a chat message.
    Enriched with workflow context so the frontend can render accordingly.
    """
    reply: str
    completion_percentage: int = 0
    requirements: dict = {}

    # --- v2.0 enrichment fields ---
    workflow_stage: str = "conversation"
    missing_requirements: list[str] = []
    validation_results: list[str] = []
    next_action: Optional[str] = None

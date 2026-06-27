"""
Session state model for AI FloorPlanner Backend.

Represents the complete state of a user session including
conversation history, collected requirements, workflow stage,
and validation results.
"""

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field

from models.requirements import Requirements, REQUIREMENT_FIELDS


class ConversationTurn(BaseModel):
    """A single turn in the conversation."""
    role: str  # 'user' | 'assistant' | 'system'
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SessionState(BaseModel):
    """
    Complete state for a single user session.
    This is the single source of truth for everything about a session.
    """

    # --- Identity ---
    session_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # --- Conversation ---
    conversation_history: list[ConversationTurn] = Field(default_factory=list)

    # --- Requirements ---
    requirements: Requirements = Field(default_factory=Requirements)

    # --- Workflow ---
    workflow_stage: str = "conversation"  # Maps to WorkflowStage enum values

    # --- Validation ---
    missing_requirements: list[str] = Field(
        default_factory=lambda: [f[0] for f in REQUIREMENT_FIELDS]
    )
    validation_results: list[str] = Field(default_factory=list)

    # --- Planning (future) ---
    planning_result: Optional[dict] = None

    # --- Metadata ---
    metadata: dict = Field(default_factory=dict)

    def append_turn(self, role: str, content: str) -> None:
        """Add a conversation turn and update timestamp."""
        self.conversation_history.append(
            ConversationTurn(role=role, content=content)
        )
        self.updated_at = datetime.now(timezone.utc)

    def get_recent_turns(self, n: int = 10) -> list[ConversationTurn]:
        """Get the most recent n conversation turns."""
        return self.conversation_history[-n:]

    def touch(self) -> None:
        """Update the last-modified timestamp."""
        self.updated_at = datetime.now(timezone.utc)

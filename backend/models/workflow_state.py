"""
WorkflowState model representing the state object passed between agents.
"""

from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from models.requirements import Requirements
from models.session import ConversationTurn


class WorkflowState(BaseModel):
    session_id: str
    conversation_history: List[ConversationTurn] = Field(default_factory=list)
    requirements: Requirements = Field(default_factory=Requirements)
    validation: Dict[str, Any] = Field(default_factory=dict)
    planning: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    current_agent: Optional[str] = None
    next_agent: Optional[str] = None
    completed_agents: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def append_message(self, role: str, content: str) -> None:
        """Append a new turn to the conversation history and update updated_at."""
        self.conversation_history.append(ConversationTurn(role=role, content=content))
        self.updated_at = datetime.now(timezone.utc)

    def update_requirements(self, reqs: Requirements) -> None:
        """Merge/Update the requirements object and update updated_at."""
        self.requirements = self.requirements.merge(reqs)
        self.updated_at = datetime.now(timezone.utc)

    def mark_agent_completed(self, agent_name: str) -> None:
        """Mark an agent as completed by appending it to completed_agents list."""
        if agent_name not in self.completed_agents:
            self.completed_agents.append(agent_name)
        self.updated_at = datetime.now(timezone.utc)

    def get_missing_fields(self) -> List[str]:
        """Get the missing required fields from the requirements object."""
        return self.requirements.missing_fields()

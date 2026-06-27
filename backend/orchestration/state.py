"""
Workflow State for AI FloorPlanner Backend.

Defines the possible stages of the workflow and rules for transitions.
"""

from enum import Enum
from dataclasses import dataclass, field


class WorkflowStage(str, Enum):
    """Enumeration of possible workflow stages."""
    CONVERSATION = "conversation"
    EXTRACTION = "extraction"
    VALIDATION = "validation"
    PLANNING = "planning"
    CAD_GENERATION = "cad_generation"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class WorkflowState:
    """Tracks the current execution state within a single request cycle."""
    stage: WorkflowStage = WorkflowStage.CONVERSATION
    errors: list[str] = field(default_factory=list)
    final_reply: str = ""
    is_finished: bool = False

    def transition_to(self, new_stage: WorkflowStage) -> None:
        """Move to a new stage."""
        self.stage = new_stage

    def finish(self, reply: str) -> None:
        """Mark the cycle as finished and store the final reply."""
        self.final_reply = reply
        self.is_finished = True

    def mark_error(self, error: str) -> None:
        """Record an error and halt execution."""
        self.errors.append(error)
        self.stage = WorkflowStage.ERROR
        self.is_finished = True

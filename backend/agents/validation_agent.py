"""
Validation Agent for AI FloorPlanner Backend.

Checks collected requirements for consistency and architectural feasibility.
"""

from typing import Optional

from agents.base_agent import BaseAgent, AgentResult
from models.session import SessionState


class ValidationAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(name="validation", **kwargs)

    async def execute(self, session: SessionState, user_message: Optional[str] = None) -> AgentResult:
        self.logger.info("Executing ValidationAgent", extra={"session_id": session.session_id})

        # Basic deterministic validation (stub for now)
        is_valid = True
        issues = []

        # Example future validation logic:
        # if session.requirements.plot_width and session.requirements.plot_length:
        #     area = session.requirements.plot_width * session.requirements.plot_length
        #     if session.requirements.bedrooms and area < session.requirements.bedrooms * 200:
        #         is_valid = False
        #         issues.append("Plot area is too small for the requested number of bedrooms.")

        session.validation_results = issues

        # Regardless of validation outcome, we go back to conversation
        # to ask the next question, unless we're complete.
        return AgentResult(
            metadata={"is_valid": is_valid, "issues": issues},
            next_action="converse"
        )

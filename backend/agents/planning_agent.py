"""
Planning Agent for AI FloorPlanner Backend.

Converts validated requirements into a structured architectural FloorplanSpec.
"""

from typing import Optional

from agents.base_agent import BaseAgent, AgentResult
from models.session import SessionState


class PlanningAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(name="planning", **kwargs)

    async def execute(self, session: SessionState, user_message: Optional[str] = None) -> AgentResult:
        self.logger.info("Executing PlanningAgent", extra={"session_id": session.session_id})

        if not session.requirements.is_complete:
            return AgentResult(
                success=False,
                error="Cannot plan without complete requirements",
                next_action="converse"
            )

        # Stub: Just store a placeholder planning result for now
        # Future: Call LLM to generate FloorplanSpec JSON
        session.planning_result = {
            "status": "planned",
            "message": "Planning complete (placeholder)",
            "inputs": session.requirements.to_summary_dict()
        }

        return AgentResult(
            reply="Your architectural plan has been generated.",
            next_action="cad_generate"
        )

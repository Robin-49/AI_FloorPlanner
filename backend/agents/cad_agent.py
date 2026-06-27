"""
CAD Generation Agent for AI FloorPlanner Backend.

Converts a FloorplanSpec into CAD instructions (DXF/SVG/IFC).
"""

from typing import Optional

from agents.base_agent import BaseAgent, AgentResult
from models.session import SessionState


class CADAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(name="cad_generation", **kwargs)

    async def execute(self, session: SessionState, user_message: Optional[str] = None) -> AgentResult:
        self.logger.info("Executing CADAgent", extra={"session_id": session.session_id})

        if not session.planning_result:
            return AgentResult(
                success=False,
                error="Cannot generate CAD without a planning result",
            )

        # Stub: Return placeholder
        return AgentResult(
            reply="CAD generation is not yet implemented.",
            metadata={"cad_format": "stub"},
            next_action="completed"
        )

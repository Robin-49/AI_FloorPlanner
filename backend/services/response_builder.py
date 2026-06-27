"""
Response Builder for AI FloorPlanner Backend.

Constructs standardized ChatMessageResponse objects from agent outputs
and the current session state.
"""

from typing import Optional

from schemas.responses import ChatMessageResponse
from models.session import SessionState


class ResponseBuilder:
    """
    Builds structured API responses from workflow state.
    Ensures the frontend gets a consistent contract regardless of which agent ran.
    """

    @staticmethod
    def build_chat_response(
        session: SessionState,
        reply: str,
        next_action: Optional[str] = None
    ) -> ChatMessageResponse:
        """
        Construct a ChatMessageResponse for the frontend.

        Args:
            session: The current updated SessionState
            reply: The message to show the user
            next_action: Optional system hint for the frontend

        Returns:
            ChatMessageResponse object
        """
        # Calculate completion percentage from requirements model
        completion_pct = session.requirements.calculate_completion()

        # Build summary dict
        requirements_summary = session.requirements.to_summary_dict()

        return ChatMessageResponse(
            reply=reply,
            completion_percentage=completion_pct,
            requirements=requirements_summary,
            workflow_stage=session.workflow_stage,
            missing_requirements=session.missing_requirements,
            validation_results=session.validation_results,
            next_action=next_action
        )

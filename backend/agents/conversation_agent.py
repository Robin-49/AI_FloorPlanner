"""
Conversation Agent for AI FloorPlanner Backend.

Decides what question to ask the user next based on missing requirements.
Currently wraps the deterministic question_engine logic to preserve behavior.
"""

from typing import Optional

from agents.base_agent import BaseAgent, AgentResult
from models.session import SessionState
from models.requirements import REQUIREMENT_FIELDS
from memory.requirement_memory import RequirementMemory


class ConversationAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(name="conversation", **kwargs)

    async def execute(self, session: SessionState, user_message: Optional[str] = None) -> AgentResult:
        self.logger.info("Executing ConversationAgent", extra={"session_id": session.session_id})

        # Recalculate missing requirements
        missing = RequirementMemory.get_missing(session)

        if not missing:
            # We have everything we need!
            return AgentResult(
                reply="Requirements collection complete.",
                next_action="plan"
            )

        # In Deterministic mode (preserving current behavior),
        # we simply pick the first missing field and ask its associated question.
        next_field = missing[0]
        next_question = self._get_question_for_field(next_field)

        # In future LLM mode, we would do this:
        # system_prompt = self.prompts.get_prompt("conversation", ...)
        # next_question = await self.llm.generate(system_prompt=system_prompt)

        return AgentResult(
            reply=next_question,
            next_action="wait_for_user"
        )

    def _get_question_for_field(self, target_field: str) -> str:
        for field, question in REQUIREMENT_FIELDS:
            if field == target_field:
                return question
        return "Can you tell me more about your requirements?"

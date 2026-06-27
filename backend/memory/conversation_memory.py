"""
Conversation Memory for AI FloorPlanner Backend.

Provides helper methods for interacting with the conversation history
stored in the SessionState.
"""

from typing import List

from models.session import SessionState, ConversationTurn
from utils.logger import get_logger

logger = get_logger("memory.conversation")


class ConversationMemory:
    """
    Manages conversation history within a session.
    """

    @staticmethod
    def add_turn(session: SessionState, role: str, content: str) -> None:
        """
        Add a new turn to the conversation history.

        Args:
            session: The active SessionState
            role: 'user', 'assistant', or 'system'
            content: The text content of the message
        """
        session.append_turn(role=role, content=content)
        logger.debug(
            f"Added {role} turn to session {session.session_id}",
            extra={"action": "add_conversation_turn"}
        )

    @staticmethod
    def get_history(session: SessionState) -> List[ConversationTurn]:
        """Get the full conversation history."""
        return session.conversation_history

    @staticmethod
    def get_recent(session: SessionState, n: int = 5) -> List[ConversationTurn]:
        """Get the most recent n conversation turns."""
        return session.get_recent_turns(n)

    @staticmethod
    def format_history_for_prompt(session: SessionState, n: int = 5) -> str:
        """
        Format the recent history as a string suitable for injection
        into an LLM prompt.
        """
        turns = session.get_recent_turns(n)
        if not turns:
            return "No previous conversation."

        formatted = []
        for turn in turns:
            formatted.append(f"{turn.role.upper()}: {turn.content}")

        return "\n\n".join(formatted)

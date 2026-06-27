"""
Base Agent protocol for AI FloorPlanner Backend.

All agents must implement this interface.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

from models.session import SessionState
from services.llm_service import BaseLLMService, get_llm_service
from services.prompt_manager import PromptManager, get_prompt_manager
from utils.logger import get_logger


@dataclass
class AgentResult:
    """Standardized output from any agent execution."""
    reply: Optional[str] = None
    next_action: Optional[str] = None
    metadata: dict = field(default_factory=dict)
    success: bool = True
    error: Optional[str] = None


class BaseAgent(ABC):
    """
    Abstract base class for all architectural agents.
    Provides shared dependencies (LLM, Prompts, Logger).
    """

    def __init__(
        self,
        name: str,
        llm_service: Optional[BaseLLMService] = None,
        prompt_manager: Optional[PromptManager] = None
    ):
        self.name = name
        self.llm = llm_service or get_llm_service()
        self.prompts = prompt_manager or get_prompt_manager()
        self.logger = get_logger(f"agents.{name}")

    @abstractmethod
    async def execute(self, session: SessionState, user_message: Optional[str] = None) -> AgentResult:
        """
        Execute the agent's primary capability.

        Args:
            session: The active SessionState (mutable)
            user_message: Optional incoming message from the user

        Returns:
            An AgentResult detailing what happened and what to do next
        """
        ...

"""
Extraction Agent for AI FloorPlanner Backend.

Extracts structured requirement values from raw user messages.
Currently uses deterministic type coercion to preserve previous behavior.
"""

from typing import Optional
import json

from agents.base_agent import BaseAgent, AgentResult
from models.session import SessionState
from memory.requirement_memory import RequirementMemory
from utils.validators import coerce_field_value
from models.requirements import Requirements
from services.llm_service import LLMService


class ExtractionAgent:

    def __init__(self):
        self.llm = LLMService()

    async def execute(
        self,
        message: str,
        requirements: Requirements
    ) -> Requirements:

        extracted = await self.llm.extract_requirements(
            message,
            requirements
        )

        return extracted
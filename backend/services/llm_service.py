"""
LLM Service abstraction for AI FloorPlanner Backend.

Provides a unified interface for calling any LLM provider.
No agent should directly call any provider — all LLM calls go through this service.

Supported providers:
    - deterministic: No LLM — uses rule-based logic (current behavior)
    - groq: Groq API (future)
    - openai: OpenAI API (future)
    - ollama: Local Ollama instance (future)
    - anthropic: Anthropic API (future)
"""

from abc import ABC, abstractmethod
from typing import Optional
import re

from utils.logger import get_logger
from models.requirements import Requirements

logger = get_logger("services.llm")


class BaseLLMService(ABC):
    """
    Abstract base class for LLM providers.
    All LLM interactions must go through an implementation of this interface.
    """

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        """
        Generate a text response from the LLM.

        Args:
            prompt: The user/input prompt
            system_prompt: Optional system instructions
            temperature: Sampling temperature (0.0 - 1.0)
            max_tokens: Maximum tokens in the response

        Returns:
            The generated text response
        """
        ...

    @abstractmethod
    def get_provider_name(self) -> str:
        """Return the name of this LLM provider."""
        ...


class DeterministicLLMService(BaseLLMService):
    """
    Non-LLM service that preserves current deterministic behavior.

    This is the default during the refactor phase — no actual LLM calls
    are made. The agents use their own rule-based logic and pass
    pre-formatted responses through this service.
    """

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        """
        In deterministic mode, the prompt IS the response.
        Agents construct the exact response they want and pass it through.
        """
        logger.debug(
            "Deterministic passthrough",
            extra={"action": "llm_generate", "agent": "deterministic"},
        )
        return prompt

    def get_provider_name(self) -> str:
        return "deterministic"


class GroqLLMService(BaseLLMService):
    """
    Groq API integration (stub — ready for implementation).

    When activated, this will use the GROQ_API_KEY from settings
    to call the Groq API for fast LLM inference.
    """

    def __init__(self, api_key: str, model: str = "llama3-8b-8192"):
        self.api_key = api_key
        self.model = model

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        # TODO: Implement actual Groq API call
        logger.warning(
            "GroqLLMService.generate() called but not yet implemented",
            extra={"action": "llm_generate_stub"},
        )
        raise NotImplementedError(
            "Groq LLM integration not yet implemented. "
            "Set LLM_PROVIDER=deterministic in .env to use rule-based mode."
        )

    def get_provider_name(self) -> str:
        return "groq"


def get_llm_service(provider: str = "deterministic", **kwargs) -> BaseLLMService:
    """
    Factory function to create the appropriate LLM service.

    Args:
        provider: The LLM provider name ('deterministic', 'groq', 'openai', etc.)
        **kwargs: Provider-specific configuration

    Returns:
        An instance of BaseLLMService
    """
    if provider == "deterministic":
        return DeterministicLLMService()
    elif provider == "groq":
        api_key = kwargs.get("api_key", "")
        model = kwargs.get("model", "llama3-8b-8192")
        return GroqLLMService(api_key=api_key, model=model)
    else:
        logger.warning(
            f"Unknown LLM provider '{provider}', falling back to deterministic",
            extra={"action": "llm_factory_fallback"},
        )
        return DeterministicLLMService()


class LLMService:
    """
    High-level LLM Service wrapper for agent workflows.
    Provides mock natural language requirement extraction.
    """

    def __init__(self, provider: str = "deterministic"):
        self.provider = get_llm_service(provider)

    async def extract_requirements(
        self,
        message: str,
        current_requirements: Requirements
    ) -> Requirements:
        """
        Mock requirement extraction.
        Analyzes raw message content and updates appropriate hierarchical fields.
        """
        extracted = Requirements(**current_requirements.model_dump())
        message_lower = message.lower()

        # Check for width x length format, e.g. "30x50", "30 x 50"
        dim_match = re.search(r'(\d+)\s*(?:x|by)\s*(\d+)', message_lower)
        if dim_match:
            extracted.site.width = float(dim_match.group(1))
            extracted.site.length = float(dim_match.group(2))
        else:
            # Handle isolated numbers by guessing based on what's missing next
            num_matches = re.findall(r'\b\d+\b', message_lower)
            if num_matches:
                val = float(num_matches[0])
                missing = current_requirements.missing_fields()
                if missing:
                    first_missing = missing[0]
                    if first_missing == "site.width":
                        extracted.site.width = val
                    elif first_missing == "site.length":
                        extracted.site.length = val
                    elif first_missing == "building.floors":
                        extracted.building.floors = int(val)
                    elif first_missing == "rooms.bedrooms":
                        extracted.rooms.bedrooms = int(val)
                    elif first_missing == "bathrooms.attached":
                        extracted.bathrooms.attached = int(val)
                    elif first_missing == "parking.covered":
                        extracted.parking.covered = int(val)

        # Facing directions
        for d in ["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest"]:
            if d in message_lower:
                extracted.site.facing = d.capitalize()
                break

        # Style
        for s in ["modern", "traditional", "contemporary", "minimalist", "industrial", "mediterranean"]:
            if s in message_lower:
                extracted.building.style = s.capitalize()
                break

        # Vastu
        if "vastu" in message_lower:
            if "yes" in message_lower or "require" in message_lower or "want" in message_lower or "true" in message_lower or "yup" in message_lower:
                extracted.building.vastu_required = True
            elif "no" in message_lower or "don't" in message_lower or "not" in message_lower or "false" in message_lower:
                extracted.building.vastu_required = False

        return extracted

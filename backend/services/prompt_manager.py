"""
Prompt management for AI FloorPlanner Backend.

Loads prompt templates from the prompts/ directory.
Supports variable injection via {variable} placeholders.
Caches loaded prompts for performance.
"""

import os
from functools import lru_cache
from typing import Optional

from utils.logger import get_logger

logger = get_logger("services.prompt_manager")


class PromptManager:
    """
    Loads and manages prompt templates from markdown files.

    Usage:
        pm = PromptManager("prompts")
        prompt = pm.get_prompt("conversation", requirements="4BHK duplex")
    """

    def __init__(self, prompts_dir: str = "prompts"):
        self.prompts_dir = prompts_dir
        self._cache: dict[str, str] = {}

    def get_prompt(self, name: str, **variables) -> str:
        """
        Load a prompt template by name and inject variables.

        Args:
            name: Prompt template name (without .md extension)
            **variables: Key-value pairs to inject into the template

        Returns:
            The rendered prompt string
        """
        template = self._load_template(name)

        # Inject variables
        if variables:
            try:
                rendered = template.format(**variables)
            except KeyError as e:
                logger.warning(
                    f"Missing variable {e} in prompt '{name}', returning raw template",
                    extra={"action": "prompt_render_warning"},
                )
                rendered = template
        else:
            rendered = template

        return rendered

    def _load_template(self, name: str) -> str:
        """Load a template from disk, using cache if available."""
        if name in self._cache:
            return self._cache[name]

        file_path = os.path.join(self.prompts_dir, f"{name}.md")

        if not os.path.exists(file_path):
            logger.warning(
                f"Prompt template not found: {file_path}",
                extra={"action": "prompt_not_found"},
            )
            return ""

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        self._cache[name] = content
        logger.debug(
            f"Loaded prompt template: {name}",
            extra={"action": "prompt_loaded"},
        )
        return content

    def clear_cache(self) -> None:
        """Clear the prompt cache (useful for development/hot-reload)."""
        self._cache.clear()

    def list_available(self) -> list[str]:
        """List all available prompt template names."""
        if not os.path.isdir(self.prompts_dir):
            return []
        return [
            f.replace(".md", "")
            for f in os.listdir(self.prompts_dir)
            if f.endswith(".md")
        ]


@lru_cache()
def get_prompt_manager(prompts_dir: str = "prompts") -> PromptManager:
    """Get a cached PromptManager singleton."""
    return PromptManager(prompts_dir)

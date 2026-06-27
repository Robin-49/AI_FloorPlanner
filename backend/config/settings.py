"""
Application settings loaded from environment variables.

Uses Pydantic Settings for validation and type coercion.
All configuration is centralized here — no hardcoded values in business logic.
"""

from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application-wide configuration."""

    # --- Application ---
    APP_NAME: str = "AI FloorPlanner"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # --- Server ---
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: list[str] = Field(default=["*"])

    # --- LLM Providers ---
    LLM_PROVIDER: str = "deterministic"  # deterministic | groq | openai | ollama
    LLM_MODEL: str = ""
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 1024

    # Provider-specific keys
    GROQ_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    ANTHROPIC_API_KEY: Optional[str] = None

    # --- Session ---
    SESSION_STORE: str = "memory"  # memory | sqlite | redis (future)
    SESSION_TTL_SECONDS: int = 3600  # 1 hour

    # --- Prompts ---
    PROMPTS_DIR: str = "prompts"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore",
    }


@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached singleton Settings instance.
    Call get_settings() anywhere to access configuration.
    """
    return Settings()

"""
Embedding Service abstraction for AI FloorPlanner Backend.

Stub service for future RAG / Vector DB integration.
Will be used to retrieve architectural rules, similar floor plans, etc.
"""

from abc import ABC, abstractmethod


class BaseEmbeddingService(ABC):
    """Abstract interface for generating embeddings."""

    @abstractmethod
    async def embed_text(self, text: str) -> list[float]:
        """Convert a text string into a vector embedding."""
        ...


class StubEmbeddingService(BaseEmbeddingService):
    """Placeholder embedding service."""

    async def embed_text(self, text: str) -> list[float]:
        """Returns a dummy embedding."""
        return [0.0] * 1536  # Default dimensionality for typical models

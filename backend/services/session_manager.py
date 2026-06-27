"""
Session management for AI FloorPlanner Backend.

Replaces the previous raw dictionary with an abstracted SessionStore
interface and an InMemorySessionStore implementation.
Provides methods to safely update the SessionState object.
"""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import uuid4

from models.session import SessionState
from utils.logger import get_logger

logger = get_logger("services.session_manager")


class SessionStore(ABC):
    """Abstract interface for session storage."""

    @abstractmethod
    def create(self, session_id: Optional[str] = None) -> SessionState:
        """Create a new session state."""
        ...

    @abstractmethod
    def get(self, session_id: str) -> Optional[SessionState]:
        """Retrieve an existing session state."""
        ...

    @abstractmethod
    def save(self, session: SessionState) -> None:
        """Save/persist a session state."""
        ...

    @abstractmethod
    def delete(self, session_id: str) -> None:
        """Delete a session state."""
        ...


class InMemorySessionStore(SessionStore):
    """
    In-memory implementation of SessionStore.
    Data is lost on server restart (preserves current behavior).
    """

    def __init__(self):
        self._sessions: dict[str, SessionState] = {}
        logger.info(
            "Initialized InMemorySessionStore",
            extra={"action": "session_store_init"},
        )

    def create(self, session_id: Optional[str] = None) -> SessionState:
        if not session_id:
            session_id = str(uuid4())

        session = SessionState(session_id=session_id)
        self._sessions[session_id] = session

        logger.info(
            f"Created new session {session_id}",
            extra={"action": "session_create", "session_id": session_id},
        )
        return session

    def get(self, session_id: str) -> Optional[SessionState]:
        session = self._sessions.get(session_id)
        if not session:
            logger.warning(
                f"Session not found: {session_id}",
                extra={"action": "session_not_found", "session_id": session_id},
            )
        return session

    def save(self, session: SessionState) -> None:
        session.touch()  # Update last modified timestamp
        self._sessions[session.session_id] = session
        logger.debug(
            f"Saved session {session.session_id}",
            extra={"action": "session_save", "session_id": session.session_id},
        )

    def delete(self, session_id: str) -> None:
        if session_id in self._sessions:
            del self._sessions[session_id]
            logger.info(
                f"Deleted session {session_id}",
                extra={"action": "session_delete", "session_id": session_id},
            )


# Global singleton instance (for in-memory store)
_store = InMemorySessionStore()


class SessionManager:
    """
    Business logic layer for session operations.
    Wraps the underlying SessionStore.
    """

    def __init__(self, store: SessionStore = _store):
        self.store = store

    def start_session(self, session_id: Optional[str] = None) -> SessionState:
        """Initialize a new session."""
        return self.store.create(session_id)

    def get_session(self, session_id: str) -> Optional[SessionState]:
        """Retrieve a session by ID."""
        return self.store.get(session_id)

    def get_or_create_session(self, session_id: str) -> SessionState:
        """Retrieve a session, creating it if it doesn't exist."""
        session = self.store.get(session_id)
        if not session:
            logger.info(
                f"Session {session_id} not found, creating new",
                extra={"action": "session_recreate", "session_id": session_id},
            )
            session = self.store.create(session_id)
        return session

    def save_session(self, session: SessionState) -> None:
        """Persist changes to a session."""
        self.store.save(session)
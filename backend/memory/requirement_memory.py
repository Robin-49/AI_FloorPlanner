"""
Requirement Memory for AI FloorPlanner Backend.

Provides helper methods for interacting with and tracking changes
to architectural requirements in the SessionState.
"""

from typing import Any

from models.session import SessionState
from models.requirements import REQUIREMENT_FIELDS
from utils.logger import get_logger

logger = get_logger("memory.requirement")


class RequirementMemory:
    """
    Manages architectural requirements within a session.
    """

    @staticmethod
    def update_field(session: SessionState, field: str, value: Any) -> bool:
        """
        Update a single requirement field.

        Args:
            session: The active SessionState
            field: The requirement field name
            value: The new value

        Returns:
            True if the field was updated, False if it was invalid or unchanged
        """
        valid_fields = {f[0] for f in REQUIREMENT_FIELDS}
        if field not in valid_fields:
            logger.warning(
                f"Attempted to update invalid requirement field: {field}",
                extra={"action": "invalid_requirement_update"}
            )
            return False

        current_value = getattr(session.requirements, field)
        if current_value == value:
            return False  # Unchanged

        setattr(session.requirements, field, value)
        session.touch()

        # If a field was successfully updated, it's no longer "missing"
        if field in session.missing_requirements:
            session.missing_requirements.remove(field)

        logger.info(
            f"Updated requirement: {field} = {value}",
            extra={"action": "requirement_updated", "field": field, "value": value}
        )
        return True

    @staticmethod
    def bulk_update(session: SessionState, updates: dict) -> int:
        """
        Update multiple requirement fields at once.

        Args:
            session: The active SessionState
            updates: Dictionary of field->value updates

        Returns:
            Number of fields successfully updated
        """
        updated_count = 0
        for field, value in updates.items():
            if RequirementMemory.update_field(session, field, value):
                updated_count += 1

        return updated_count

    @staticmethod
    def get_missing(session: SessionState) -> list[str]:
        """
        Recalculate and return missing requirements.
        Also updates the session.missing_requirements list.
        """
        missing = session.requirements.get_missing_fields()
        session.missing_requirements = missing
        return missing

    @staticmethod
    def is_complete(session: SessionState) -> bool:
        """Check if all requirements have been gathered."""
        return session.requirements.is_complete

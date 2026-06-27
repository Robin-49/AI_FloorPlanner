"""
Structured logging for AI FloorPlanner Backend.

Provides JSON-formatted log output with contextual fields
for session tracking, agent identification, and performance monitoring.
"""

import logging
import json
import sys
from datetime import datetime, timezone
from typing import Optional


class StructuredFormatter(logging.Formatter):
    """
    Formats log records as JSON for structured logging.
    Includes contextual fields when provided via the `extra` parameter.
    """

    CONTEXT_FIELDS = [
        "session_id",
        "agent",
        "workflow_stage",
        "completion_pct",
        "execution_time_ms",
        "action",
        "requirements_collected",
        "next_action",
    ]

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Attach contextual fields if present
        for field in self.CONTEXT_FIELDS:
            value = getattr(record, field, None)
            if value is not None:
                log_entry[field] = value

        # Attach exception info if present
        if record.exc_info and record.exc_info[1]:
            log_entry["error"] = str(record.exc_info[1])
            log_entry["error_type"] = type(record.exc_info[1]).__name__

        return json.dumps(log_entry, default=str)


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Creates or retrieves a named logger with structured JSON output.

    Args:
        name: Logger name (typically module path, e.g. 'agents.conversation')
        level: Optional override for log level (DEBUG, INFO, WARNING, ERROR)

    Returns:
        Configured logging.Logger instance
    """
    logger = logging.getLogger(f"floorplanner.{name}")

    # Avoid adding duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(StructuredFormatter())
        logger.addHandler(handler)

    if level:
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    elif not logger.level:
        logger.setLevel(logging.INFO)

    return logger

"""
Input validation and sanitization utilities for AI FloorPlanner Backend.

Extracted from the inline parsing logic that was previously in api/chat.py.
"""

from typing import Optional


# Fields that should be parsed as integers
NUMERIC_FIELDS = frozenset([
    "plot_width",
    "plot_length",
    "floors",
    "bedrooms",
    "bathrooms",
    "parking_spaces",
])

# Fields that should be parsed as booleans
BOOLEAN_FIELDS = frozenset([
    "vastu_required",
])


def parse_int_safe(value: str) -> Optional[int]:
    """
    Safely parse a string to an integer.
    Returns None if the string cannot be parsed.

    Args:
        value: The string to parse

    Returns:
        Parsed integer or None
    """
    try:
        return int(value.strip())
    except (ValueError, AttributeError):
        return None


def parse_bool_safe(value: str) -> Optional[bool]:
    """
    Parse a user input string into a boolean.
    Handles common affirmative/negative phrases.

    Args:
        value: The string to parse

    Returns:
        Parsed boolean or None if ambiguous
    """
    clean = value.strip().lower()
    if clean in ("yes", "y", "true", "1", "yeah", "yep", "sure"):
        return True
    if clean in ("no", "n", "false", "0", "nah", "nope"):
        return False
    return None


def sanitize_input(value: str) -> str:
    """
    Sanitize user input by stripping whitespace and
    removing potentially dangerous characters.

    Args:
        value: Raw user input

    Returns:
        Sanitized string
    """
    if not isinstance(value, str):
        return str(value)
    return value.strip()


def coerce_field_value(field: str, raw_value: str):
    """
    Coerce a raw string value to the appropriate type for a given field.

    Args:
        field: The requirement field name
        raw_value: The raw user input string

    Returns:
        The coerced value (int, bool, or str)
    """
    sanitized = sanitize_input(raw_value)

    if field in NUMERIC_FIELDS:
        parsed = parse_int_safe(sanitized)
        if parsed is not None:
            return parsed
        return sanitized  # Return as-is if can't parse

    if field in BOOLEAN_FIELDS:
        parsed = parse_bool_safe(sanitized)
        if parsed is not None:
            return parsed
        return sanitized

    return sanitized

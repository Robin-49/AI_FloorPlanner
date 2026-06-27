"""
General-purpose helper utilities for AI FloorPlanner Backend.
"""

import time
from uuid import uuid4
from typing import Optional


def generate_id(prefix: Optional[str] = None) -> str:
    """
    Generate a unique ID string, optionally with a prefix.

    Args:
        prefix: Optional prefix like 'session', 'msg', 'agent'

    Returns:
        A unique string ID, e.g. 'session_a1b2c3d4...'
    """
    uid = uuid4().hex
    if prefix:
        return f"{prefix}_{uid}"
    return uid


class TimingContext:
    """
    Context manager for measuring execution time in milliseconds.

    Usage:
        with TimingContext() as timer:
            do_work()
        print(f"Took {timer.elapsed_ms}ms")
    """

    def __init__(self):
        self.start_time: float = 0.0
        self.end_time: float = 0.0
        self.elapsed_ms: float = 0.0

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        self.elapsed_ms = round((self.end_time - self.start_time) * 1000, 2)
        return False

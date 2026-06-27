"""
Floorplan specification model for AI FloorPlanner Backend.

Stub model for future CAD generation. Represents the output
of the Planning Agent — a structured architectural specification.
"""

from typing import Optional

from pydantic import BaseModel, Field


class RoomSpec(BaseModel):
    """Specification for a single room in the floor plan."""
    name: str
    room_type: str  # bedroom, bathroom, kitchen, living, etc.
    area_sqft: Optional[float] = None
    width: Optional[float] = None
    length: Optional[float] = None
    floor: int = 0


class FloorplanSpec(BaseModel):
    """
    Structured architectural specification produced by the Planning Agent.
    This is the input to the CAD Generation Agent.
    """
    rooms: list[RoomSpec] = Field(default_factory=list)
    stairs: Optional[dict] = None
    parking: Optional[dict] = None
    setbacks: Optional[dict] = None
    total_built_area_sqft: Optional[float] = None
    metadata: dict = Field(default_factory=dict)

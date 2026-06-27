"""
Hierarchical architectural requirements model for AI FloorPlanner Backend.
"""

from pydantic import BaseModel, Field
from typing import Optional, Any


class SiteRequirements(BaseModel):
    width: Optional[float] = None
    length: Optional[float] = None
    area: Optional[float] = None
    facing: Optional[str] = None
    corner_plot: Optional[bool] = None


class BuildingRequirements(BaseModel):
    house_type: Optional[str] = None
    floors: Optional[int] = None
    style: Optional[str] = None
    vastu_required: Optional[bool] = None


class RoomRequirements(BaseModel):
    bedrooms: Optional[int] = None
    living_rooms: Optional[int] = None
    pooja_room: Optional[bool] = None
    study_room: Optional[bool] = None
    home_office: Optional[bool] = None


class KitchenRequirements(BaseModel):
    count: Optional[int] = None
    type: Optional[str] = None  # open, closed, utility-attached


class BathroomRequirements(BaseModel):
    attached: Optional[int] = None
    common: Optional[int] = None


class ParkingRequirements(BaseModel):
    covered: Optional[int] = None
    open_spaces: Optional[int] = None
    bike_parking: Optional[int] = None


class OutdoorRequirements(BaseModel):
    garden: Optional[bool] = None
    balcony: Optional[bool] = None
    terrace: Optional[bool] = None


class BudgetRequirements(BaseModel):
    construction_budget: Optional[float] = None


class ConstraintRequirements(BaseModel):
    max_height: Optional[float] = None
    setbacks_front: Optional[float] = None
    setbacks_rear: Optional[float] = None


class PreferenceRequirements(BaseModel):
    natural_lighting: Optional[str] = None  # high, medium, low
    ventilation: Optional[str] = None


class ProjectRequirements(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class Requirements(BaseModel):
    project: ProjectRequirements = Field(default_factory=ProjectRequirements)
    site: SiteRequirements = Field(default_factory=SiteRequirements)
    building: BuildingRequirements = Field(default_factory=BuildingRequirements)
    rooms: RoomRequirements = Field(default_factory=RoomRequirements)
    kitchen: KitchenRequirements = Field(default_factory=KitchenRequirements)
    bathrooms: BathroomRequirements = Field(default_factory=BathroomRequirements)
    parking: ParkingRequirements = Field(default_factory=ParkingRequirements)
    outdoor: OutdoorRequirements = Field(default_factory=OutdoorRequirements)
    budget: BudgetRequirements = Field(default_factory=BudgetRequirements)
    constraints: ConstraintRequirements = Field(default_factory=ConstraintRequirements)
    preferences: PreferenceRequirements = Field(default_factory=PreferenceRequirements)

    def merge(self, other: "Requirements") -> "Requirements":
        """
        Merge another Requirements object into this one, overwriting None values
        and prioritizing the other's non-None values.
        """
        merged_data = {}
        for field_name in self.model_fields.keys():
            self_section = getattr(self, field_name)
            other_section = getattr(other, field_name)
            
            section_data = {}
            for subfield in self_section.model_fields.keys():
                self_val = getattr(self_section, subfield)
                other_val = getattr(other_section, subfield)
                section_data[subfield] = other_val if other_val is not None else self_val
            
            merged_data[field_name] = self_section.__class__(**section_data)
        
        return Requirements(**merged_data)

    def missing_fields(self) -> list[str]:
        """
        Returns a list of missing required fields using hierarchical dot notation.
        Required core fields:
        - site.width
        - site.length
        - site.facing
        - building.floors
        - rooms.bedrooms
        - bathrooms.attached
        - parking.covered
        - building.vastu_required
        - building.style
        """
        required_mappings = [
            ("site.width", self.site.width),
            ("site.length", self.site.length),
            ("site.facing", self.site.facing),
            ("building.floors", self.building.floors),
            ("rooms.bedrooms", self.rooms.bedrooms),
            ("bathrooms.attached", self.bathrooms.attached),
            ("parking.covered", self.parking.covered),
            ("building.vastu_required", self.building.vastu_required),
            ("building.style", self.building.style),
        ]
        return [field_path for field_path, val in required_mappings if val is None]

    def completion_percentage(self) -> int:
        """Calculate the completion percentage of the required fields."""
        required_fields_count = 9
        missing = len(self.missing_fields())
        completed = required_fields_count - missing
        return round((completed / required_fields_count) * 100)

    def to_summary(self) -> dict:
        """
        Flatten the hierarchical requirements for backward compatibility with the frontend.
        """
        # Map hierarchical fields back to the old flat names that the UI expects
        return {
            "plot_width": self.site.width,
            "plot_length": self.site.length,
            "facing_direction": self.site.facing,
            "floors": self.building.floors,
            "bedrooms": self.rooms.bedrooms,
            "bathrooms": (self.bathrooms.attached or 0) + (self.bathrooms.common or 0) if (self.bathrooms.attached is not None or self.bathrooms.common is not None) else None,
            "parking_spaces": (self.parking.covered or 0) + (self.parking.open_spaces or 0) if (self.parking.covered is not None or self.parking.open_spaces is not None) else None,
            "vastu_required": self.building.vastu_required,
            "style": self.building.style,
        }
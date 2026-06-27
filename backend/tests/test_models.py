"""
Unit tests for backend requirements and session models.
"""

from models.requirements import Requirements
from models.session import SessionState


def test_requirements_completion():
    reqs = Requirements()
    assert reqs.calculate_completion() == 0
    assert not reqs.is_complete
    assert len(reqs.get_missing_fields()) == 9

    reqs.plot_width = 30
    assert reqs.calculate_completion() == 11
    assert not reqs.is_complete

    # Fill all fields
    reqs.plot_length = 40
    reqs.facing_direction = "North"
    reqs.floors = 2
    reqs.bedrooms = 3
    reqs.bathrooms = 3
    reqs.parking_spaces = 1
    reqs.vastu_required = True
    reqs.style = "Modern"

    assert reqs.calculate_completion() == 100
    assert reqs.is_complete
    assert len(reqs.get_missing_fields()) == 0


def test_session_state_turn_appending():
    session = SessionState(session_id="test_session")
    assert len(session.conversation_history) == 0

    session.append_turn("user", "Hello")
    assert len(session.conversation_history) == 1
    assert session.conversation_history[0].role == "user"
    assert session.conversation_history[0].content == "Hello"

"""
Unit tests for individual agents.
"""

import pytest
from models.session import SessionState
from agents.conversation_agent import ConversationAgent
from agents.extraction_agent import ExtractionAgent
from agents.validation_agent import ValidationAgent


@pytest.mark.asyncio
async def test_conversation_agent():
    agent = ConversationAgent()
    session = SessionState(session_id="test")
    session.missing_requirements = ["plot_width", "plot_length"]

    result = await agent.execute(session)
    assert result.success
    assert "plot width" in result.reply.lower()
    assert result.next_action == "wait_for_user"


@pytest.mark.asyncio
async def test_extraction_agent():
    agent = ExtractionAgent()
    session = SessionState(session_id="test")
    session.missing_requirements = ["plot_width", "plot_length"]

    # Test extracting width from input "30"
    result = await agent.execute(session, "30")
    assert result.success
    assert session.requirements.plot_width == 30
    assert result.next_action == "validate"


@pytest.mark.asyncio
async def test_validation_agent():
    agent = ValidationAgent()
    session = SessionState(session_id="test")

    result = await agent.execute(session)
    assert result.success
    assert result.next_action == "converse"

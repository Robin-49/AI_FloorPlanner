"""
Integration tests for workflow orchestration.
"""

import pytest
from orchestration.workflow import WorkflowOrchestrator
from services.session_manager import SessionManager


@pytest.mark.asyncio
async def test_workflow_orchestrator_full_flow():
    orchestrator = WorkflowOrchestrator()
    session_manager = SessionManager()
    session_id = "test_workflow"

    # Start by sending width
    response = await orchestrator.process_message(session_id, "30")
    assert response.completion_percentage > 0
    assert response.requirements["plot_width"] == 30
    assert "plot length" in response.reply.lower()

    # Load session and check state
    session = session_manager.get_session(session_id)
    assert session is not None
    assert session.requirements.plot_width == 30
    assert len(session.conversation_history) == 2  # user + assistant turn

"""
Session API Router for AI FloorPlanner Backend.

Handles creating new sessions.
"""

from fastapi import APIRouter, HTTPException

from schemas.responses import StartSessionResponse
from services.session_manager import SessionManager
from memory.conversation_memory import ConversationMemory
from utils.logger import get_logger

logger = get_logger("api.session")
router = APIRouter(tags=["session"])

session_manager = SessionManager()


@router.post("/start-session", response_model=StartSessionResponse)
async def start_session():
    """
    Initialize a new architectural design session.
    """
    logger.info("Received request to start a new session")
    try:
        # Create session state
        session = session_manager.start_session()

        # The initial greeting (in v1 this was hardcoded in the endpoint)
        # We store it in memory so it's part of the conversation history
        reply = "Welcome to AI_FloorPlanner. What is the plot width in feet?"
        ConversationMemory.add_turn(session, "assistant", reply)

        session_manager.save_session(session)

        return StartSessionResponse(
            session_id=session.session_id,
            reply=reply,
            workflow_stage=session.workflow_stage
        )
    except Exception as e:
        logger.error(f"Error starting session: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
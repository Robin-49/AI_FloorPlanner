"""
Chat API Router for AI FloorPlanner Backend.

Thin layer that handles HTTP requests and delegates all business logic
to the WorkflowOrchestrator.
"""

from fastapi import APIRouter, HTTPException

from schemas.requests import ChatMessageRequest
from schemas.responses import ChatMessageResponse
from orchestration.workflow import WorkflowOrchestrator
from utils.logger import get_logger

logger = get_logger("api.chat")
router = APIRouter(tags=["chat"])

# Initialize the orchestrator once
orchestrator = WorkflowOrchestrator()


@router.post("/chat", response_model=ChatMessageResponse)
async def chat_endpoint(request: ChatMessageRequest):
    """
    Process an incoming chat message and advance the workflow.
    """
    logger.info(f"Received chat request for session {request.session_id}")
    try:
        response = await orchestrator.process_message(
            session_id=request.session_id,
            message=request.message
        )
        return response
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
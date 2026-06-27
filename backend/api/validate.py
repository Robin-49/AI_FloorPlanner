"""
Validate API Router for AI FloorPlanner Backend.

Standalone endpoint to trigger the validation agent manually.
"""

from fastapi import APIRouter, HTTPException

from schemas.requests import ValidateRequest
from schemas.responses import ValidationResponse
from services.session_manager import SessionManager
from agents.validation_agent import ValidationAgent
from utils.logger import get_logger

logger = get_logger("api.validate")
router = APIRouter(tags=["validate"])

session_manager = SessionManager()
validation_agent = ValidationAgent()


@router.post("/validate", response_model=ValidationResponse)
async def validate_endpoint(request: ValidateRequest):
    """
    Manually trigger validation on the current session requirements.
    """
    logger.info(f"Received manual validation request for session {request.session_id}")
    try:
        session = session_manager.get_session(request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Execute just the validation agent
        result = await validation_agent.execute(session)

        # The agent updates session.validation_results
        is_valid = result.metadata.get("is_valid", True)
        issues = result.metadata.get("issues", [])
        
        session_manager.save_session(session)

        return ValidationResponse(
            session_id=session.session_id,
            is_valid=is_valid,
            issues=issues,
            missing_requirements=session.missing_requirements
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating session: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

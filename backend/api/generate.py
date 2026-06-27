"""
Generate API Router for AI FloorPlanner Backend.

Standalone endpoint to trigger the planning and CAD generation agents.
"""

from fastapi import APIRouter, HTTPException

from schemas.requests import GenerateRequest
from services.session_manager import SessionManager
from agents.planning_agent import PlanningAgent
from agents.cad_agent import CADAgent
from utils.logger import get_logger

logger = get_logger("api.generate")
router = APIRouter(tags=["generate"])

session_manager = SessionManager()
planning_agent = PlanningAgent()
cad_agent = CADAgent()


@router.post("/generate-floorplan")
async def generate_endpoint(request: GenerateRequest):
    """
    Generate an architectural floor plan from collected requirements.
    """
    logger.info(f"Received generation request for session {request.session_id}")
    try:
        session = session_manager.get_session(request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        if not session.requirements.is_complete:
            raise HTTPException(
                status_code=400, 
                detail=f"Cannot generate floor plan. Missing requirements: {session.missing_requirements}"
            )

        # 1. Run Planning Agent
        plan_result = await planning_agent.execute(session)
        if not plan_result.success:
            raise HTTPException(status_code=500, detail=plan_result.error)

        # 2. Run CAD Agent
        cad_result = await cad_agent.execute(session)
        if not cad_result.success:
            raise HTTPException(status_code=500, detail=cad_result.error)

        session_manager.save_session(session)

        return {
            "status": "success",
            "session_id": session.session_id,
            "message": cad_result.reply,
            "cad_format": cad_result.metadata.get("cad_format"),
            "planning_result": session.planning_result
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating floor plan: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

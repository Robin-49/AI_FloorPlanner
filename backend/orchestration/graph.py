"""
Agent Execution Graph for AI FloorPlanner Backend.

Registers all agents and provides them to the Router.
Designed to be easily swappable with LangGraph in the future.
"""

from agents.conversation_agent import ConversationAgent
from agents.extraction_agent import ExtractionAgent
from agents.validation_agent import ValidationAgent
from agents.planning_agent import PlanningAgent
from agents.cad_agent import CADAgent
from orchestration.state import WorkflowStage


def build_agent_graph() -> dict:
    """
    Instantiate all agents and map them to their corresponding WorkflowStage.

    Returns:
        A dictionary mapping WorkflowStage to BaseAgent instances.
    """
    return {
        WorkflowStage.CONVERSATION: ConversationAgent(),
        WorkflowStage.EXTRACTION: ExtractionAgent(),
        WorkflowStage.VALIDATION: ValidationAgent(),
        WorkflowStage.PLANNING: PlanningAgent(),
        WorkflowStage.CAD_GENERATION: CADAgent(),
    }

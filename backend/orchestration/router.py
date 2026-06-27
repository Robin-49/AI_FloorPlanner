"""
Agent Router for AI FloorPlanner Backend.

Determines which agent should execute next based on the WorkflowStage
and the results of the previous agent's execution.
"""

from agents.base_agent import BaseAgent
from orchestration.state import WorkflowStage
from utils.logger import get_logger

logger = get_logger("orchestration.router")


class AgentRouter:
    """Routes execution to the appropriate agent."""

    def __init__(self, agents: dict[WorkflowStage, BaseAgent]):
        self.agents = agents

    def get_agent_for_stage(self, stage: WorkflowStage) -> BaseAgent:
        """Retrieve the agent responsible for a specific stage."""
        agent = self.agents.get(stage)
        if not agent:
            raise ValueError(f"No agent registered for stage: {stage}")
        return agent

    def determine_next_stage(
        self,
        current_stage: WorkflowStage,
        next_action_hint: str
    ) -> WorkflowStage:
        """
        Determine the next WorkflowStage based on current state and agent hints.

        Args:
            current_stage: The stage that just completed
            next_action_hint: Hint provided by the agent's AgentResult

        Returns:
            The next WorkflowStage to execute
        """
        if next_action_hint == "wait_for_user":
            # The agent asked a question, we must pause execution and wait for the frontend
            return current_stage

        if current_stage == WorkflowStage.CONVERSATION:
            if next_action_hint == "plan":
                return WorkflowStage.PLANNING
            # Typically, conversation doesn't transition on its own without user input,
            # but if we're processing a user message, we go to extraction first.
            return WorkflowStage.EXTRACTION

        elif current_stage == WorkflowStage.EXTRACTION:
            # After extracting data from user input, always validate
            return WorkflowStage.VALIDATION

        elif current_stage == WorkflowStage.VALIDATION:
            # After validating, go back to conversation to ask the next question
            return WorkflowStage.CONVERSATION

        elif current_stage == WorkflowStage.PLANNING:
            return WorkflowStage.CAD_GENERATION

        elif current_stage == WorkflowStage.CAD_GENERATION:
            return WorkflowStage.COMPLETED

        logger.warning(
            f"Unhandled transition from {current_stage} with hint '{next_action_hint}'",
            extra={"action": "unhandled_transition"}
        )
        return WorkflowStage.ERROR

"""
Workflow Orchestrator for AI FloorPlanner Backend.

The central brain of the backend. It receives requests from the API,
loads the session, coordinates agent execution via the Router, and
builds the final response.
"""

from typing import Optional

from models.session import SessionState
from schemas.responses import ChatMessageResponse
from orchestration.state import WorkflowState, WorkflowStage
from orchestration.router import AgentRouter
from orchestration.graph import build_agent_graph
from services.session_manager import SessionManager
from services.response_builder import ResponseBuilder
from memory.conversation_memory import ConversationMemory
from utils.logger import get_logger

logger = get_logger("orchestration.workflow")


class WorkflowOrchestrator:
    """Coordinates the entire request/response lifecycle."""

    def __init__(self, session_manager: Optional[SessionManager] = None):
        self.session_manager = session_manager or SessionManager()
        self.router = AgentRouter(build_agent_graph())

    async def process_message(self, session_id: str, message: str) -> ChatMessageResponse:
        """
        Process an incoming chat message through the agent pipeline.

        Args:
            session_id: The user's session ID
            message: The raw text message from the user

        Returns:
            A constructed ChatMessageResponse
        """
        logger.info(
            f"Processing message for session {session_id}",
            extra={"action": "process_message_start", "session_id": session_id}
        )

        # 1. Load State
        session = self.session_manager.get_or_create_session(session_id)

        # 2. Record User Input
        ConversationMemory.add_turn(session, "user", message)

        # 3. Initialize Execution State
        # We start at EXTRACTION because we just received a user message
        # that needs to be parsed for requirements.
        exec_state = WorkflowState(stage=WorkflowStage.EXTRACTION)

        # 4. Execute Pipeline Loop
        max_iterations = 5
        iterations = 0

        while not exec_state.is_finished and iterations < max_iterations:
            iterations += 1
            current_stage = exec_state.stage
            logger.debug(f"Executing stage: {current_stage.value}")

            # Get the right agent
            agent = self.router.get_agent_for_stage(current_stage)

            # Execute the agent
            try:
                result = await agent.execute(session, message)

                if not result.success:
                    exec_state.mark_error(result.error or "Agent execution failed")
                    break

                # If the agent wants to reply to the user, we pause the pipeline
                if result.next_action == "wait_for_user":
                    if result.reply:
                        ConversationMemory.add_turn(session, "assistant", result.reply)
                        exec_state.finish(result.reply)
                    else:
                        exec_state.mark_error("Agent requested wait without providing a reply")
                    break

                # Determine next stage based on agent's hint
                next_stage = self.router.determine_next_stage(current_stage, result.next_action or "")

                if next_stage == WorkflowStage.COMPLETED:
                    if result.reply:
                        ConversationMemory.add_turn(session, "assistant", result.reply)
                        exec_state.finish(result.reply)
                    else:
                        exec_state.finish("Workflow completed.")
                    break
                elif next_stage == WorkflowStage.ERROR:
                    exec_state.mark_error(f"Invalid transition from {current_stage}")
                    break
                else:
                    exec_state.transition_to(next_stage)

            except Exception as e:
                logger.error(
                    f"Error executing agent {agent.name}: {str(e)}",
                    exc_info=True,
                    extra={"action": "agent_error", "session_id": session_id}
                )
                exec_state.mark_error(f"Internal error: {str(e)}")

        # 5. Handle infinite loops or errors
        if not exec_state.is_finished:
            logger.error("Pipeline reached max iterations", extra={"session_id": session_id})
            exec_state.mark_error("Max pipeline iterations reached")

        if exec_state.errors:
            final_reply = f"I'm sorry, I encountered an error: {exec_state.errors[0]}"
            ConversationMemory.add_turn(session, "system", final_reply)
        else:
            final_reply = exec_state.final_reply

        # 6. Update session tracking
        session.workflow_stage = exec_state.stage.value
        self.session_manager.save_session(session)

        # 7. Build Response
        return ResponseBuilder.build_chat_response(session, final_reply)

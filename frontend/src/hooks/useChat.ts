import { useContext, useEffect } from "react";
import { ChatContext } from "@/store/chatStore";
import { chatService } from "@/services/chatService";

export function useChat() {
  const context = useContext(ChatContext);

  if (!context) {
    throw new Error(
      "useChat must be used within a ChatStoreProvider"
    );
  }

  const {
    messages,
    isLoading,
    completionStatus,
    progress,
    workflowStage,
    collectedRequirements,
    addMessage,
    setLoading,
    setProgress,
    setWorkflowStage,
    setCompletionStatus,
    updateRequirementState,
    sessionId,
    setSessionId,
  } = context;

  useEffect(() => {
    if (sessionId) return;

    const initializeSession = async () => {
      try {
        setLoading(true);
        const data = await chatService.startSession();

        setSessionId(data.session_id);
        setWorkflowStage(data.workflow_stage);
        setProgress(0);

        if (messages.length === 0) {
          addMessage(
            data.reply,
            "assistant"
          );
        }
      } catch (error) {
        console.error(
          "Failed to start session",
          error
        );
      } finally {
        setLoading(false);
      }
    };

    initializeSession();
  }, [sessionId]);

  const sendMessage = async (
    content: string
  ) => {
    if (
      !content.trim() ||
      isLoading ||
      completionStatus === "completed"
    ) {
      return;
    }

    addMessage(content, "user");
    setLoading(true);

    try {
      const response = await chatService.sendMessage(
        sessionId,
        content
      );

      // Update state from backend response
      setProgress(response.completion_percentage);
      setWorkflowStage(response.workflow_stage);
      updateRequirementState(response.requirements);

      if (response.reply === "Requirements collection complete." || response.next_action === "plan") {
        setCompletionStatus("completed");
        addMessage(
          response.reply,
          "assistant",
          "summary" // Signal to display the final summary component
        );
      } else {
        addMessage(
          response.reply,
          "assistant"
        );
      }

      console.log(
        "Backend Response:",
        response
      );
    } catch (error: any) {
      addMessage(
        error.message ||
        "Failed to contact backend",
        "system"
      );
    } finally {
      setLoading(false);
    }
  };

  return {
    messages,
    isLoading,
    completionStatus,
    progress,
    workflowStage,
    collectedRequirements,
    sendMessage,
  };
}

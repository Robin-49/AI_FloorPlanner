"use client";

import React, { createContext, useState, ReactNode } from 'react';
import { ChatMessage, Role } from '@/types/chat';
import { ArchitectureRequirement, defaultArchitectureRequirement } from '@/types/requirement';

interface ChatStore {
  messages: ChatMessage[];
  sessionId: string;
  setSessionId: (id: string) => void;

  collectedRequirements: ArchitectureRequirement;
  completionStatus: 'in_progress' | 'completed';
  isLoading: boolean;
  progress: number;
  workflowStage: string;

  addMessage: (
    content: string,
    role: Role,
    type?: 'text' | 'summary'
  ) => void;

  updateRequirementState: (
    newReqs: ArchitectureRequirement
  ) => void;

  setProgress: (p: number) => void;
  setWorkflowStage: (stage: string) => void;
  setCompletionStatus: (status: 'in_progress' | 'completed') => void;
  resetConversation: () => void;
  setLoading: (loading: boolean) => void;
}

export const ChatContext = createContext<ChatStore | null>(null);

export function ChatStoreProvider({ children }: { children: ReactNode }) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [sessionId, setSessionId] = useState<string>("");

  const [collectedRequirements, setCollectedRequirements] = useState<ArchitectureRequirement>(defaultArchitectureRequirement);
  const [completionStatus, setCompletionStatus] = useState<'in_progress' | 'completed'>('in_progress');
  const [isLoading, setIsLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [workflowStage, setWorkflowStage] = useState('conversation');

  const addMessage = (content: string, role: Role, type: 'text' | 'summary' = 'text') => {
    setMessages(prev => [...prev, {
      id: Date.now().toString(),
      role,
      content,
      timestamp: new Date(),
      metadata: { type }
    }]);
  };

  const updateRequirementState = (newReqs: ArchitectureRequirement) => {
    setCollectedRequirements(newReqs);
  };

  const resetConversation = () => {
    setMessages([]);
    setCollectedRequirements(defaultArchitectureRequirement);
    setCompletionStatus('in_progress');
    setIsLoading(false);
    setProgress(0);
    setWorkflowStage('conversation');
    setSessionId(""); // Clear session to trigger a new session init
  };

  return (
    <ChatContext.Provider value={{
      messages,
      sessionId,
      setSessionId,

      collectedRequirements,
      completionStatus,
      isLoading,
      progress,
      workflowStage,

      addMessage,
      updateRequirementState,
      setProgress,
      setWorkflowStage,
      setCompletionStatus,
      resetConversation,
      setLoading: setIsLoading
    }}>
      {children}
    </ChatContext.Provider>
  );
}

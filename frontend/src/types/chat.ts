export type Role = 'user' | 'assistant' | 'system';

export interface ChatMessage {
  id: string;
  role: Role;
  content: string;
  timestamp: Date;
  metadata?: Record<string, any>;
}

export interface ChatSession {
  id: string;
  messages: ChatMessage[];
  createdAt: Date;
  updatedAt: Date;
}

export interface ChatMessageResponse {
  reply: string;
  completion_percentage: number;
  requirements: Record<string, any>;
  workflow_stage: string;
  missing_requirements: string[];
  validation_results: string[];
  next_action?: string | null;
}

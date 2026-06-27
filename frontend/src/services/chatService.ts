import api from './api';
import { ChatMessageResponse } from '@/types/chat';

export interface StartSessionResponse {
  session_id: string;
  reply: string;
  workflow_stage: string;
}

export const chatService = {
  async startSession(): Promise<StartSessionResponse> {
    const response = await api.post('/start-session');
    return response.data;
  },

  async sendMessage(
    sessionId: string,
    message: string
  ): Promise<ChatMessageResponse> {
    const response = await api.post('/chat', {
      session_id: sessionId,
      message,
    });

    return response.data;
  },
};
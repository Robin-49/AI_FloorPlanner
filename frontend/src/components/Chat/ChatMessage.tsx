"use client";

import React from 'react';
import { User, Bot } from 'lucide-react';
import { ChatMessage as ChatMessageType } from '@/types/chat';
import { cn } from '@/lib/utils';
import { RequirementSummary } from './RequirementSummary';
import { useChat } from '@/hooks/useChat';

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const { collectedRequirements } = useChat();
  const isUser = message.role === 'user';
  
  const formattedTime = new Date(message.timestamp).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
  });

  return (
    <div className={cn("flex w-full", isUser ? "justify-end" : "justify-start")}>
      <div className={cn("flex max-w-[85%] md:max-w-[75%] gap-3 w-full", isUser ? "flex-row-reverse" : "flex-row")}>
        
        <div className={cn(
          "flex items-center justify-center w-8 h-8 rounded-full shrink-0 mt-1 shadow-sm",
          isUser ? "bg-primary text-primary-foreground" : "bg-secondary text-secondary-foreground"
        )}>
          {isUser ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
        </div>
        
        <div className={cn("flex flex-col flex-1", isUser ? "items-end" : "items-start")}>
          {message.metadata?.type === 'summary' ? (
            <div className="w-full flex flex-col gap-4">
              <div className="px-4 py-3 rounded-2xl shadow-sm text-sm md:text-base leading-relaxed whitespace-pre-wrap bg-muted text-foreground rounded-tl-sm w-fit">
                {message.content}
              </div>
              <RequirementSummary requirements={collectedRequirements} className="w-full max-w-2xl" />
            </div>
          ) : (
            <div className={cn(
              "px-4 py-3 rounded-2xl shadow-sm text-sm md:text-base leading-relaxed whitespace-pre-wrap",
              isUser 
                ? "bg-primary text-primary-foreground rounded-tr-sm" 
                : "bg-muted text-foreground rounded-tl-sm"
            )}>
              {message.content}
            </div>
          )}
          
          <span className="text-[10px] text-muted-foreground mt-1.5 px-1">
            {formattedTime}
          </span>
        </div>
        
      </div>
    </div>
  );
}

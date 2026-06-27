"use client";

import React from 'react';
import { useChat } from '@/hooks/useChat';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { WelcomeScreen } from './WelcomeScreen';
import { ProgressTracker } from './ProgressTracker';

export function ChatContainer() {
  const { messages, isLoading, progress, collectedRequirements, completionStatus } = useChat();
  const messagesEndRef = React.useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  React.useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const totalQuestions = 9;
  const answeredQuestions = Object.keys(collectedRequirements).filter(
    key => collectedRequirements[key as keyof typeof collectedRequirements] !== undefined && collectedRequirements[key as keyof typeof collectedRequirements] !== null
  ).length;
  const remaining = Math.max(0, totalQuestions - answeredQuestions);

  return (
    <div className="flex flex-col h-full bg-background">
      <div className="flex-1 overflow-y-auto p-4 md:p-8">
        {messages.length === 0 ? (
          <WelcomeScreen />
        ) : (
          <div className="max-w-4xl mx-auto space-y-6 pb-4">
            <ProgressTracker progress={progress} remainingQuestions={remaining} className="mb-6" />
            
            {messages.map((msg) => (
              <ChatMessage key={msg.id} message={msg} />
            ))}
            
            {isLoading && (
              <div className="flex w-full justify-start">
                <div className="flex max-w-[80%] gap-4 flex-row">
                  <div className="flex items-center justify-center w-8 h-8 rounded-full shrink-0 bg-secondary text-secondary-foreground">
                    <div className="w-5 h-5 flex items-center justify-center animate-pulse">...</div>
                  </div>
                  <div className="flex flex-col">
                    <div className="p-4 rounded-2xl rounded-tl-sm bg-muted animate-pulse">
                      <div className="space-y-2 w-48">
                        <div className="h-4 bg-background/50 rounded w-3/4"></div>
                        <div className="h-4 bg-background/50 rounded w-1/2"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>
      
      {completionStatus !== 'completed' && (
        <div className="p-4 bg-background/95 backdrop-blur border-t border-border">
          <div className="max-w-4xl mx-auto">
            <ChatInput />
          </div>
        </div>
      )}
    </div>
  );
}

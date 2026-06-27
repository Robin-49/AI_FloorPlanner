"use client";

import React, { useState } from 'react';
import { SendHorizontal } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useChat } from '@/hooks/useChat';

export function ChatInput() {
  const [input, setInput] = useState('');
  const { sendMessage, isLoading } = useChat();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    
    sendMessage(input.trim());
    setInput('');
  };

  return (
    <form onSubmit={handleSubmit} className="relative flex items-center w-full">
      <Input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Describe your ideal floor plan requirements..."
        className="pr-12 h-14 text-base rounded-full border-border bg-background focus-visible:ring-primary shadow-sm"
        disabled={isLoading}
      />
      <Button 
        type="submit" 
        size="icon" 
        disabled={!input.trim() || isLoading}
        className="absolute right-2 rounded-full w-10 h-10 bg-primary hover:bg-primary/90 text-primary-foreground"
      >
        <SendHorizontal className="w-5 h-5" />
      </Button>
    </form>
  );
}

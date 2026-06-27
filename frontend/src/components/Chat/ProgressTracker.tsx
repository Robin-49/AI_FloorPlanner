"use client";

import React from 'react';
import { cn } from '@/lib/utils';

interface ProgressTrackerProps {
  progress: number; // 0 to 100
  remainingQuestions: number;
  className?: string;
}

export function ProgressTracker({ progress, remainingQuestions, className }: ProgressTrackerProps) {
  // Ensure progress stays strictly between 0 and 100
  const clampedProgress = Math.max(0, Math.min(100, Math.round(progress)));

  return (
    <div className={cn("w-full bg-card border rounded-xl p-4 shadow-sm", className)}>
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-medium text-foreground">
          Requirement Progress
        </span>
        <span className="text-sm font-bold text-primary">
          {clampedProgress}%
        </span>
      </div>
      
      {/* Progress Bar Container */}
      <div className="relative h-2 w-full bg-muted rounded-full overflow-hidden">
        {/* Animated Progress Fill */}
        <div 
          className="absolute top-0 left-0 h-full bg-primary transition-all duration-500 ease-out rounded-full"
          style={{ width: `${clampedProgress}%` }}
        />
      </div>

      <div className="mt-2 text-xs text-muted-foreground flex justify-between items-center">
        <span>Validation Status</span>
        <span className="font-medium">
          {remainingQuestions > 0 
            ? `${remainingQuestions} question${remainingQuestions === 1 ? '' : 's'} remaining` 
            : 'All requirements collected!'}
        </span>
      </div>
    </div>
  );
}

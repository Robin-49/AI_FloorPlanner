"use client";

import React from 'react';
import { Compass, Box, PenTool } from 'lucide-react';

export function WelcomeScreen() {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center space-y-8 animate-in fade-in zoom-in duration-500">
      <div className="space-y-4">
        <div className="mx-auto w-20 h-20 bg-primary/10 rounded-2xl flex items-center justify-center">
          <Compass className="w-10 h-10 text-primary" />
        </div>
        <h1 className="text-4xl font-bold tracking-tight text-foreground">
          AI_FloorPlanner
        </h1>
        <p className="text-xl text-muted-foreground max-w-[600px] mx-auto">
          Your personal AI Architect Assistant. Describe your requirements to generate beautiful, validated floor plans.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl w-full text-left">
        <div className="p-6 rounded-xl border bg-card text-card-foreground shadow-sm">
          <PenTool className="w-6 h-6 text-primary mb-4" />
          <h3 className="font-semibold mb-2">1. Specify Requirements</h3>
          <p className="text-sm text-muted-foreground">Tell me about your desired space, budget, and style preferences.</p>
        </div>
        <div className="p-6 rounded-xl border bg-card text-card-foreground shadow-sm">
          <Box className="w-6 h-6 text-primary mb-4" />
          <h3 className="font-semibold mb-2">2. Review & Refine</h3>
          <p className="text-sm text-muted-foreground">I will validate your requirements and draft an initial layout.</p>
        </div>
      </div>
    </div>
  );
}

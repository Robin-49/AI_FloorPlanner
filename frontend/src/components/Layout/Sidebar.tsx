"use client";

import React from 'react';
import { Settings, FolderOpen, History } from 'lucide-react';
import { Button } from '@/components/ui/button';

export function Sidebar() {
  return (
    <aside className="hidden md:flex w-64 flex-col border-r border-border bg-muted/20 h-[calc(100vh-3.5rem)]">
      <div className="flex h-full flex-col gap-4 p-4">
        <div className="flex-1 space-y-4">
          <div className="space-y-2">
            <h2 className="text-sm font-semibold tracking-tight">Previous Plans</h2>
            <div className="space-y-1">
              <Button variant="ghost" className="w-full justify-start text-muted-foreground hover:text-foreground">
                <History className="mr-2 h-4 w-4" />
                Modern Villa
              </Button>
              <Button variant="ghost" className="w-full justify-start text-muted-foreground hover:text-foreground">
                <History className="mr-2 h-4 w-4" />
                Office Space 204
              </Button>
            </div>
          </div>
          <div className="space-y-2">
            <h2 className="text-sm font-semibold tracking-tight">Projects</h2>
            <Button variant="ghost" className="w-full justify-start text-muted-foreground hover:text-foreground">
              <FolderOpen className="mr-2 h-4 w-4" />
              Browse All
            </Button>
          </div>
        </div>
        <div className="mt-auto">
          <Button variant="ghost" className="w-full justify-start text-muted-foreground hover:text-foreground">
            <Settings className="mr-2 h-4 w-4" />
            Settings
          </Button>
        </div>
      </div>
    </aside>
  );
}

"use client";

import React from 'react';
import { ArchitectureRequirement } from '@/types/requirement';
import { Map, Home, LayoutGrid, Sparkles, Check, Minus } from 'lucide-react';
import { cn } from '@/lib/utils';

interface RequirementSummaryProps {
  requirements: ArchitectureRequirement;
  className?: string;
}

export function RequirementSummary({ requirements, className }: RequirementSummaryProps) {
  // Helper component for sections
  const Section = ({ title, icon: Icon, children }: { title: string, icon: any, children: React.ReactNode }) => (
    <div className="space-y-3">
      <div className="flex items-center gap-2 text-primary font-semibold border-b pb-2">
        <Icon className="w-4 h-4" />
        <h3 className="text-sm uppercase tracking-wider">{title}</h3>
      </div>
      <div className="grid grid-cols-2 gap-x-4 gap-y-3 text-sm">
        {children}
      </div>
    </div>
  );

  // Helper component for rendering individual properties
  const Item = ({ label, value }: { label: string, value: string | number | boolean | undefined }) => {
    let displayValue: React.ReactNode = value;
    
    if (typeof value === 'boolean') {
      displayValue = value ? (
        <span className="flex items-center gap-1 text-green-600 dark:text-green-500 font-medium"><Check className="w-4 h-4" /> Yes</span>
      ) : (
        <span className="flex items-center gap-1 text-muted-foreground"><Minus className="w-4 h-4" /> No</span>
      );
    } else if (value === 0 || value === '' || value === undefined || value === null) {
      displayValue = <span className="text-muted-foreground italic">Pending</span>;
    }

    return (
      <div className="flex flex-col">
        <span className="text-muted-foreground text-xs mb-0.5">{label}</span>
        <span className="font-medium text-foreground">{displayValue}</span>
      </div>
    );
  };

  return (
    <div className={cn("bg-card text-card-foreground border rounded-xl shadow-sm p-6 space-y-6 w-full", className)}>
      <div className="text-lg font-bold tracking-tight">Project Summary</div>
      
      <Section title="Plot Information" icon={Map}>
        <Item 
          label="Dimensions" 
          value={(requirements.plot_width && requirements.plot_length) ? `${requirements.plot_width} x ${requirements.plot_length} ft` : ''} 
        />
        <Item label="Facing" value={requirements.facing_direction} />
      </Section>

      <Section title="Building Details" icon={Home}>
        <Item label="Floors" value={requirements.floors} />
      </Section>

      <Section title="Rooms" icon={LayoutGrid}>
        <Item label="Bedrooms" value={requirements.bedrooms} />
        <Item label="Bathrooms" value={requirements.bathrooms} />
        <Item label="Parking Spaces" value={requirements.parking_spaces} />
      </Section>

      <Section title="Preferences" icon={Sparkles}>
        <Item label="Style" value={requirements.style} />
        <Item label="Vastu Required" value={requirements.vastu_required} />
      </Section>
    </div>
  );
}

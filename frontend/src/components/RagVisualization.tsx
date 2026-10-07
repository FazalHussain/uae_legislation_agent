import { useState } from 'react';
import { cn } from '@/lib/utils';
import type { RagStep } from '@/types';
import {
  ChevronDown,
  ChevronRight,
  Search,
  Layers,
  ListFilter,
  ArrowUpDown,
  FileStack,
  Clock,
} from 'lucide-react';

interface RagVisualizationProps {
  steps: RagStep[];
}

const STEP_ICONS = [Search, Layers, ListFilter, ArrowUpDown, FileStack];

const STEP_COLORS = [
  'text-blue-600 bg-blue-50 ring-blue-200',
  'text-indigo-600 bg-indigo-50 ring-indigo-200',
  'text-cyan-600 bg-cyan-50 ring-cyan-200',
  'text-uae-green-dark bg-uae-green/10 ring-uae-green/25',
  'text-navy-700 bg-navy-50 ring-navy-200',
];

export function RagVisualization({ steps }: RagVisualizationProps) {
  const [expandedSteps, setExpandedSteps] = useState<Set<number>>(new Set([0]));

  const toggleStep = (index: number) => {
    setExpandedSteps((prev) => {
      const next = new Set(prev);
      if (next.has(index)) {
        next.delete(index);
      } else {
        next.add(index);
      }
      return next;
    });
  };

  return (
    <div className="mt-4 rounded-xl border border-dashed border-navy-200/60 bg-navy-50/40 overflow-hidden">
      {/* Header */}
      <div className="flex items-center gap-2 px-3.5 py-2.5 border-b border-dashed border-navy-200/60 bg-navy-50/60">
        <div className="flex h-6 w-6 items-center justify-center rounded-md bg-navy-900">
          <Layers className="h-3.5 w-3.5 text-uae-green-light" />
        </div>
        <span className="text-xs font-semibold text-navy-800 uppercase tracking-wide">
          RAG Pipeline
        </span>
        <span className="text-[10px] text-navy-600/60 ml-auto font-mono">
          {steps.reduce((acc, s) => acc + parseFloat(s.duration), 0).toFixed(2)}s total
        </span>
      </div>

      {/* Pipeline steps */}
      <div className="p-3 space-y-1.5">
        {steps.map((step, index) => {
          const Icon = STEP_ICONS[index] || Search;
          const colorClass = STEP_COLORS[index] || STEP_COLORS[0];
          const isExpanded = expandedSteps.has(index);

          return (
            <div key={index} className="rounded-lg bg-card border border-border/60 overflow-hidden">
              {/* Step header */}
              <button
                onClick={() => toggleStep(index)}
                className="flex w-full items-center gap-2.5 px-3 py-2 hover:bg-muted/50 transition-colors text-left"
              >
                {/* Step number + icon */}
                <div className={cn('flex h-7 w-7 shrink-0 items-center justify-center rounded-md ring-1', colorClass)}>
                  <Icon className="h-3.5 w-3.5" />
                </div>

                {/* Label + description */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-mono text-muted-foreground/60">
                      {String(index + 1).padStart(2, '0')}
                    </span>
                    <span className="text-sm font-medium text-foreground truncate">
                      {step.label}
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground truncate mt-0.5">
                    {step.description}
                  </p>
                </div>

                {/* Duration */}
                <span className="flex items-center gap-1 text-[10px] font-mono text-muted-foreground/70 shrink-0">
                  <Clock className="h-2.5 w-2.5" />
                  {step.duration}
                </span>

                {/* Chevron */}
                {isExpanded ? (
                  <ChevronDown className="h-4 w-4 text-muted-foreground shrink-0" />
                ) : (
                  <ChevronRight className="h-4 w-4 text-muted-foreground shrink-0" />
                )}
              </button>

              {/* Step content */}
              {isExpanded && (
                <div className="border-t border-border/40 px-3 py-2.5 space-y-1.5 animate-fade-in">
                  {/* Items count */}
                  <p className="text-[10px] uppercase tracking-wider text-muted-foreground/50 font-medium mb-1">
                    {step.items.length} {step.items.length === 1 ? 'item' : 'items'}
                  </p>

                  {step.items.map((item, i) => (
                    <div
                      key={item.id}
                      className="flex items-center gap-2 rounded-md bg-muted/40 px-2.5 py-1.5 hover:bg-muted/70 transition-colors"
                      style={{ animationDelay: `${i * 0.03}s` }}
                    >
                      {/* Score badge */}
                      {item.score !== undefined && (
                        <div className="flex items-center gap-1 shrink-0">
                          <div className="w-12 h-1.5 rounded-full bg-muted overflow-hidden">
                            <div
                              className="h-full rounded-full bg-uae-green"
                              style={{ width: `${Math.round(item.score * 100)}%` }}
                            />
                          </div>
                          <span className="text-[10px] font-mono text-muted-foreground tabular-nums w-8">
                            {item.score.toFixed(2)}
                          </span>
                        </div>
                      )}

                      {/* Item text */}
                      <div className="flex-1 min-w-0">
                        <p className="text-xs font-medium text-foreground truncate">
                          {item.title}
                        </p>
                        <p className="text-[10px] text-muted-foreground truncate">
                          {item.subtitle}
                        </p>
                      </div>

                      {/* Metadata */}
                      {item.metadata && (
                        <span className="text-[10px] text-muted-foreground/60 shrink-0 font-mono">
                          {item.metadata}
                        </span>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Flow visualization */}
      <div className="px-3 pb-3">
        <div className="flex items-center gap-1 text-[10px] text-muted-foreground/60 font-mono">
          {steps.map((step, i) => (
            <span key={i} className="flex items-center gap-1">
              <span className={cn(
                'rounded px-1.5 py-0.5',
                i === steps.length - 1 ? 'bg-uae-green/10 text-uae-green-dark' : 'bg-muted'
              )}>
                {step.label.split(' ')[0]}
              </span>
              {i < steps.length - 1 && <span className="text-muted-foreground/30">→</span>}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

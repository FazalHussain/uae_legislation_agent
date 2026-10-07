import { useState } from 'react';
import { Collapsible, CollapsibleTrigger, CollapsibleContent } from '@/components/ui/collapsible';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import type { LegalSource } from '@/types';
import {
  ChevronDown,
  FileText,
  ExternalLink,
  Gavel,
  Scale,
} from 'lucide-react';

interface SourcesSectionProps {
  sources: LegalSource[];
  onSourceClick: (source: LegalSource) => void;
}

function getRelevanceColor(score: number): { bg: string; text: string; bar: string; label: string } {
  if (score >= 0.9) return { bg: 'bg-uae-green/10', text: 'text-uae-green-dark', bar: 'bg-uae-green', label: 'Very High' };
  if (score >= 0.8) return { bg: 'bg-uae-green/8', text: 'text-uae-green-dark', bar: 'bg-uae-green-light', label: 'High' };
  if (score >= 0.6) return { bg: 'bg-amber-50', text: 'text-amber-700', bar: 'bg-amber-400', label: 'Medium' };
  return { bg: 'bg-muted', text: 'text-muted-foreground', bar: 'bg-muted-foreground/40', label: 'Low' };
}

export function SourcesSection({ sources, onSourceClick }: SourcesSectionProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <Collapsible open={isOpen} onOpenChange={setIsOpen} className="mt-4">
      <CollapsibleTrigger asChild>
        <button
          className={cn(
            'flex w-full items-center justify-between rounded-lg border border-border bg-card px-3 py-2.5 text-left transition-all',
            'hover:border-uae-green/30 hover:bg-card/80 group'
          )}
        >
          <div className="flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-md bg-navy-50">
              <FileText className="h-3.5 w-3.5 text-navy-700" />
            </div>
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-foreground">Sources Used</span>
              <Badge variant="secondary" className="text-[10px] h-5 px-1.5 font-medium">
                {sources.length}
              </Badge>
            </div>
          </div>
          <ChevronDown
            className={cn(
              'h-4 w-4 text-muted-foreground transition-transform duration-200',
              isOpen && 'rotate-180'
            )}
          />
        </button>
      </CollapsibleTrigger>

      <CollapsibleContent className="mt-2.5">
        <div className="space-y-2.5 animate-fade-in">
          {sources.map((source, index) => {
            const relevance = getRelevanceColor(source.relevanceScore);
            const percentage = Math.round(source.relevanceScore * 100);

            return (
              <div
                key={source.id}
                className={cn(
                  'group rounded-xl border border-border bg-card p-3.5 transition-all hover:shadow-sm hover:border-uae-green/25'
                )}
                style={{ animationDelay: `${index * 0.05}s` }}
              >
                {/* Header */}
                <div className="flex items-start justify-between gap-2 mb-2">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-1.5 mb-1">
                      <Gavel className="h-3.5 w-3.5 text-uae-green shrink-0" />
                      <span className="text-xs font-medium text-muted-foreground">
                        {source.articleNumber}
                      </span>
                      <span className={cn('text-[10px] px-1.5 py-0.5 rounded-full font-medium', relevance.bg, relevance.text)}>
                        {relevance.label}
                      </span>
                    </div>
                    <h4 className="text-sm font-semibold text-foreground leading-snug">
                      {source.articleTitle}
                    </h4>
                    <p className="text-xs text-muted-foreground mt-0.5 truncate">
                      {source.lawName}
                    </p>
                  </div>
                </div>

                {/* Relevant text */}
                <div className="my-2.5 rounded-lg bg-muted/50 px-3 py-2 border-l-2 border-uae-green/30">
                  <p className="text-xs text-foreground/80 leading-relaxed italic font-serif">
                    "{source.relevantText}"
                  </p>
                </div>

                {/* Footer: relevance bar + view button */}
                <div className="flex items-center justify-between gap-3">
                  {/* Relevance indicator */}
                  <div className="flex items-center gap-2 flex-1 min-w-0">
                    <div className="flex-1 h-1.5 rounded-full bg-muted overflow-hidden max-w-[120px]">
                      <div
                        className={cn('h-full rounded-full transition-all duration-500', relevance.bar)}
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                    <span className="text-[11px] font-medium text-muted-foreground tabular-nums">
                      {percentage}%
                    </span>
                  </div>

                  {/* View Article button */}
                  <button
                    onClick={() => onSourceClick(source)}
                    className="flex items-center gap-1.5 rounded-lg border border-border px-2.5 py-1.5 text-xs font-medium text-foreground hover:bg-navy-900 hover:text-white hover:border-navy-900 transition-all group/btn"
                  >
                    <Scale className="h-3 w-3 text-uae-green group-hover/btn:text-uae-green-light" />
                    <span>View Article</span>
                    <ExternalLink className="h-3 w-3 opacity-50 group-hover/btn:opacity-80" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </CollapsibleContent>
    </Collapsible>
  );
}

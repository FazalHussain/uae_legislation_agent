import { ScrollArea } from '@/components/ui/scroll-area';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import type { LegalSource } from '@/types';
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
} from '@/components/ui/sheet';
import {
  X,
  Gavel,
  Calendar,
  Landmark,
  FileText,
  Scale,
  BookOpen,
  Copy,
  Check,
} from 'lucide-react';
import { useState } from 'react';

interface DocumentDrawerProps {
  source: LegalSource | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function DocumentDrawer({ source, open, onOpenChange }: DocumentDrawerProps) {
  const [copied, setCopied] = useState(false);

  if (!source) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(source.fullArticleText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent
        side="right"
        className="w-full sm:max-w-lg md:max-w-xl lg:max-w-2xl p-0 flex flex-col"
      >
        {/* Header */}
        <div className="border-b border-border px-5 py-4 bg-gradient-to-br from-navy-50 to-background">
          <SheetHeader className="space-y-3 text-left">
            <div className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-navy-900">
                <Scale className="h-4.5 w-4.5 text-uae-green-light" />
              </div>
              <div>
                <SheetTitle className="text-base font-semibold text-foreground">
                  {source.articleTitle}
                </SheetTitle>
                <SheetDescription className="text-xs">
                  {source.articleNumber}
                </SheetDescription>
              </div>
            </div>
          </SheetHeader>

          {/* Metadata badges */}
          <div className="flex flex-wrap gap-2 mt-3">
            <Badge variant="secondary" className="gap-1 text-xs font-normal">
              <Gavel className="h-3 w-3" />
              {source.lawNumber}/{source.year}
            </Badge>
            <Badge variant="secondary" className="gap-1 text-xs font-normal">
              <Landmark className="h-3 w-3" />
              {source.jurisdiction}
            </Badge>
            <Badge variant="secondary" className="gap-1 text-xs font-normal">
              <BookOpen className="h-3 w-3" />
              {source.category}
            </Badge>
          </div>
        </div>

        {/* Law name banner */}
        <div className="px-5 py-3 bg-navy-900/5 border-b border-border">
          <p className="text-xs text-muted-foreground uppercase tracking-wide font-medium mb-0.5">
            Legislation
          </p>
          <p className="text-sm font-medium text-foreground font-serif">
            {source.lawName}
          </p>
        </div>

        {/* Content */}
        <ScrollArea className="flex-1 scrollbar-thin">
          <div className="px-5 py-5">
            {/* Relevant excerpt highlight */}
            <div className="mb-5 rounded-xl border border-uae-green/25 bg-uae-green/5 p-4">
              <div className="flex items-center gap-1.5 mb-2">
                <FileText className="h-3.5 w-3.5 text-uae-green-dark" />
                <span className="text-xs font-semibold text-uae-green-dark uppercase tracking-wide">
                  Relevant Excerpt
                </span>
              </div>
              <p className="text-sm text-foreground/90 leading-relaxed italic font-serif">
                "{source.relevantText}"
              </p>
              <div className="flex items-center gap-2 mt-3">
                <div className="flex-1 h-1.5 rounded-full bg-muted overflow-hidden">
                  <div
                    className="h-full rounded-full bg-uae-green"
                    style={{ width: `${Math.round(source.relevanceScore * 100)}%` }}
                  />
                </div>
                <span className="text-xs font-medium text-uae-green-dark tabular-nums">
                  {Math.round(source.relevanceScore * 100)}% match
                </span>
              </div>
            </div>

            {/* Full article text */}
            <div className="mb-4 flex items-center justify-between">
              <h3 className="text-sm font-semibold text-foreground flex items-center gap-1.5">
                <FileText className="h-4 w-4 text-muted-foreground" />
                Full Article Text
              </h3>
              <Button
                variant="ghost"
                size="sm"
                onClick={handleCopy}
                className="h-7 gap-1.5 text-xs text-muted-foreground hover:text-foreground"
              >
                {copied ? (
                  <>
                    <Check className="h-3 w-3 text-uae-green" />
                    <span className="text-uae-green">Copied</span>
                  </>
                ) : (
                  <>
                    <Copy className="h-3 w-3" />
                    Copy
                  </>
                )}
              </Button>
            </div>

            <div className="rounded-xl border border-border bg-card p-5">
              <pre className="whitespace-pre-wrap text-sm leading-relaxed text-foreground/90 font-serif">
                {source.fullArticleText}
              </pre>
            </div>

            {/* Disclaimer */}
            <p className="text-xs text-muted-foreground/70 mt-5 text-center">
              This text is provided for research purposes. Always consult the official gazette for authoritative versions.
            </p>
          </div>
        </ScrollArea>
      </SheetContent>
    </Sheet>
  );
}

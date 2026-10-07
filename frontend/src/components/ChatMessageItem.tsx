import { useState } from 'react';
import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { cn } from '@/lib/utils';
import type { ChatMessage, LegalSource } from '@/types';
import { SourcesSection } from './SourcesSection';
import { RagVisualization } from './RagVisualization';
import { Scale, AlertCircle, Copy, Check, RefreshCw } from 'lucide-react';

interface ChatMessageItemProps {
  message: ChatMessage;
  showRagVisualization: boolean;
  onSourceClick: (source: LegalSource) => void;
  onRetry?: () => void;
}

export function ChatMessageItem({
  message,
  showRagVisualization,
  onSourceClick,
  onRetry,
}: ChatMessageItemProps) {
  const [copied, setCopied] = useState(false);
  const isUser = message.role === 'user';

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (isUser) {
    return (
      <div className="flex justify-end px-3 sm:px-4 py-3 animate-fade-in-up">
        <div className="max-w-[80%] sm:max-w-[70%]">
          <div className="rounded-2xl rounded-br-md bg-navy-900 text-white px-4 py-3 shadow-sm">
            <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="px-3 sm:px-4 py-4 animate-fade-in-up">
      <div className="max-w-3xl mx-auto">
        {/* Assistant avatar */}
        <div className="flex items-start gap-3">
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-navy-800 to-navy-950 ring-1 ring-uae-green/20 shadow-sm">
            <Scale className="h-4.5 w-4.5 text-uae-green-light" />
          </div>

          <div className="flex-1 min-w-0">
            {/* Error state */}
            {message.isError ? (
              <div className="rounded-xl border border-destructive/30 bg-destructive/5 p-4">
                <div className="flex items-start gap-2.5">
                  <AlertCircle className="h-5 w-5 text-destructive shrink-0 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-destructive">Unable to generate response</p>
                    <p className="text-sm text-muted-foreground mt-1">
                      Something went wrong while processing your request. Please try again.
                    </p>
                    {onRetry && (
                      <button
                        onClick={onRetry}
                        className="mt-3 inline-flex items-center gap-1.5 text-sm font-medium text-uae-green hover:text-uae-green-dark transition-colors"
                      >
                        <RefreshCw className="h-3.5 w-3.5" />
                        Try again
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ) : message.isThinking ? (
              <ThinkingIndicator />
            ) : (
              <>
                {/* Markdown content */}
                <div className="prose-legal text-sm text-foreground">
                  <Markdown remarkPlugins={[remarkGfm]}>{message.content || ''}</Markdown>
                  {message.isStreaming && (
                    <span className="inline-block w-1.5 h-4 bg-uae-green ml-0.5 animate-pulse-dot rounded-sm align-middle" />
                  )}
                </div>

                {/* Action bar */}
                {!message.isStreaming && !message.isError && message.content && (
                  <div className="flex items-center gap-1 mt-3 -ml-1">
                    <button
                      onClick={handleCopy}
                      className="flex items-center gap-1.5 rounded-md px-2 py-1 text-xs text-muted-foreground hover:bg-muted hover:text-foreground transition-colors"
                    >
                      {copied ? (
                        <>
                          <Check className="h-3.5 w-3.5 text-uae-green" />
                          <span className="text-uae-green">Copied</span>
                        </>
                      ) : (
                        <>
                          <Copy className="h-3.5 w-3.5" />
                          <span>Copy</span>
                        </>
                      )}
                    </button>
                  </div>
                )}

                {/* Sources */}
                {message.sources && message.sources.length > 0 && !message.isStreaming && (
                  <SourcesSection sources={message.sources} onSourceClick={onSourceClick} />
                )}

                {/* RAG Visualization */}
                {showRagVisualization && message.ragSteps && !message.isStreaming && (
                  <RagVisualization steps={message.ragSteps} />
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function ThinkingIndicator() {
  const steps = [
    'Searching legislation corpus...',
    'Retrieving relevant articles...',
    'Analyzing legal provisions...',
    'Synthesizing response...',
  ];

  return (
    <div className="flex items-start gap-3">
      <div className="flex-1">
        <div className="flex items-center gap-2 mb-3">
          <div className="flex gap-1">
            <span className="h-2 w-2 rounded-full bg-uae-green animate-pulse-dot" style={{ animationDelay: '0s' }} />
            <span className="h-2 w-2 rounded-full bg-uae-green animate-pulse-dot" style={{ animationDelay: '0.2s' }} />
            <span className="h-2 w-2 rounded-full bg-uae-green animate-pulse-dot" style={{ animationDelay: '0.4s' }} />
          </div>
          <span className="text-sm text-muted-foreground font-medium">Researching...</span>
        </div>
        <div className="space-y-2">
          {steps.map((step, i) => (
            <div
              key={i}
              className="flex items-center gap-2 animate-fade-in"
              style={{ animationDelay: `${i * 0.3}s`, opacity: 0 }}
            >
              <div className="h-1.5 w-1.5 rounded-full bg-uae-green/40" />
              <span className="text-xs text-muted-foreground">{step}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

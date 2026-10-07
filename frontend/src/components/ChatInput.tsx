import { useRef, useEffect, useState } from 'react';
import { cn } from '@/lib/utils';
import { ArrowUp, Square } from 'lucide-react';

interface ChatInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  disabled: boolean;
  isStreaming: boolean;
  onStop: () => void;
}

export function ChatInput({
  value,
  onChange,
  onSubmit,
  disabled,
  isStreaming,
  onStop,
}: ChatInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [isFocused, setIsFocused] = useState(false);

  useEffect(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;
    textarea.style.height = '0px';
    const newHeight = Math.min(textarea.scrollHeight, 200);
    textarea.style.height = `${newHeight}px`;
  }, [value]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (value.trim() && !disabled) {
        onSubmit();
      }
    }
  };

  return (
    <div className="px-3 sm:px-4 pb-3 sm:pb-4 pt-2 bg-gradient-to-t from-background via-background to-transparent">
      <div className="max-w-3xl mx-auto">
        <div
          className={cn(
            'relative flex items-end gap-2 rounded-2xl border bg-card shadow-sm transition-all duration-200',
            isFocused
              ? 'border-uae-green/40 ring-2 ring-uae-green/10 shadow-md'
              : 'border-border hover:border-border/80'
          )}
        >
          <textarea
            ref={textareaRef}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={handleKeyDown}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder="Ask about UAE legislation..."
            rows={1}
            className="flex-1 resize-none bg-transparent px-4 py-3.5 text-sm text-foreground placeholder:text-muted-foreground/60 focus:outline-none scrollbar-thin max-h-[200px]"
            style={{ minHeight: '48px' }}
          />
          <div className="p-2">
            {isStreaming ? (
              <button
                onClick={onStop}
                className="flex h-8 w-8 items-center justify-center rounded-lg bg-navy-800 text-white hover:bg-navy-900 transition-colors"
                aria-label="Stop generating"
              >
                <Square className="h-3.5 w-3.5 fill-current" />
              </button>
            ) : (
              <button
                onClick={onSubmit}
                disabled={!value.trim() || disabled}
                className={cn(
                  'flex h-8 w-8 items-center justify-center rounded-lg transition-all',
                  value.trim() && !disabled
                    ? 'bg-uae-green text-white hover:bg-uae-green-dark shadow-sm'
                    : 'bg-muted text-muted-foreground/40 cursor-not-allowed'
                )}
                aria-label="Send message"
              >
                <ArrowUp className="h-4 w-4" />
              </button>
            )}
          </div>
        </div>
        <p className="text-[11px] text-muted-foreground/50 text-center mt-2">
          Press Enter to send · Shift+Enter for new line
        </p>
      </div>
    </div>
  );
}

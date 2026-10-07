import { cn } from '@/lib/utils';
import type { ExampleQuestion } from '@/types';
import {
  Building2,
  Users,
  TrendingUp,
  Receipt,
  Scale,
  Sparkles,
  ArrowRight,
} from 'lucide-react';

interface WelcomeScreenProps {
  onQuestionClick: (question: string) => void;
  examples: ExampleQuestion[];
}

const ICON_MAP: Record<string, React.ElementType> = {
  Building2,
  Users,
  TrendingUp,
  Receipt,
};

export function WelcomeScreen({ onQuestionClick, examples }: WelcomeScreenProps) {
  return (
    <div className="flex flex-1 items-center justify-center px-4 py-8 overflow-y-auto scrollbar-thin">
      <div className="w-full max-w-3xl mx-auto">
        {/* Logo / Brand */}
        <div className="flex flex-col items-center text-center mb-10 animate-fade-in-up">
          <div className="relative mb-5">
            <div className="absolute inset-0 bg-uae-green/20 blur-2xl rounded-full" />
            <div className="relative flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-navy-800 to-navy-950 ring-1 ring-uae-green/30 shadow-xl">
              <Scale className="h-8 w-8 text-uae-green-light" />
            </div>
          </div>

          <h1 className="text-3xl sm:text-4xl font-semibold text-navy-900 tracking-tight text-balance">
            UAE Legislation AI
          </h1>
          <p className="mt-3 text-base sm:text-lg text-muted-foreground max-w-xl text-balance">
            Understand UAE legislation with AI-powered legal research.
          </p>

          <div className="flex items-center gap-2 mt-5">
            <span className="inline-flex items-center gap-1.5 rounded-full bg-uae-green/8 px-3 py-1 text-xs font-medium text-uae-green-dark ring-1 ring-uae-green/20">
              <Sparkles className="h-3 w-3" />
              Federal Laws · Executive Regulations · Free Zone Rules
            </span>
          </div>
        </div>

        {/* Example Questions */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 animate-fade-in-up" style={{ animationDelay: '0.1s', opacity: 0 }}>
          {examples.map((example) => {
            const Icon = ICON_MAP[example.icon] || Building2;
            return (
              <button
                key={example.id}
                onClick={() => onQuestionClick(example.question)}
                className={cn(
                  'group relative flex flex-col gap-3 rounded-xl border border-border bg-card p-4 text-left',
                  'hover:border-uae-green/40 hover:shadow-md transition-all duration-200',
                  'hover:-translate-y-0.5'
                )}
              >
                <div className="flex items-center justify-between">
                  <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-navy-50 group-hover:bg-uae-green/10 transition-colors">
                    <Icon className="h-4.5 w-4.5 text-navy-700 group-hover:text-uae-green transition-colors" />
                  </div>
                  <ArrowRight className="h-4 w-4 text-muted-foreground/40 group-hover:text-uae-green group-hover:translate-x-0.5 transition-all" />
                </div>
                <div>
                  <p className="text-sm font-medium text-foreground leading-snug">
                    {example.question}
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">{example.category}</p>
                </div>
              </button>
            );
          })}
        </div>

        {/* Disclaimer */}
        <p className="text-center text-xs text-muted-foreground/70 mt-8 max-w-lg mx-auto">
          This tool provides legal information for research purposes only and does not constitute legal advice.
        </p>
      </div>
    </div>
  );
}

export interface LegalSource {
  id: string;
  lawName: string;
  lawNumber: string;
  year: number;
  articleNumber: string;
  articleTitle: string;
  relevantText: string;
  fullArticleText: string;
  relevanceScore: number; // 0-1
  category: string;
  jurisdiction: string;
}

export type MessageRole = 'user' | 'assistant';

export interface RagStep {
  label: string;
  description: string;
  items: RagStepItem[];
  duration: string;
}

export interface RagStepItem {
  id: string;
  title: string;
  subtitle: string;
  score?: number;
  metadata?: string;
}

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  sources?: LegalSource[];
  ragSteps?: RagStep[];
  isStreaming?: boolean;
  isThinking?: boolean;
  isError?: boolean;
  timestamp: number;
}

export interface Conversation {
  id: string;
  title: string;
  messages: ChatMessage[];
  createdAt: number;
  updatedAt: number;
}

export interface ExampleQuestion {
  id: string;
  question: string;
  category: string;
  icon: string;
}

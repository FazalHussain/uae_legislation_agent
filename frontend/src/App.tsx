import { useState, useRef, useEffect, useCallback } from 'react';
import { Sidebar } from '@/components/Sidebar';
import { WelcomeScreen } from '@/components/WelcomeScreen';
import { ChatInput } from '@/components/ChatInput';
import { ChatMessageItem } from '@/components/ChatMessageItem';
import { DocumentDrawer } from '@/components/DocumentDrawer';
import { EXAMPLE_QUESTIONS, getMockResponse, generateMessageId, generateConversationId } from '@/data/mockData';
import type { Conversation, ChatMessage, LegalSource } from '@/types';
import { Menu, Scale, Code2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { getResponse } from './api/legislation_api';

export default function App() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);
  const [inputValue, setInputValue] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [developerMode, setDeveloperMode] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [drawerSource, setDrawerSource] = useState<LegalSource | null>(null);
  const [drawerOpen, setDrawerOpen] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const streamingRef = useRef(false);
  const streamTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const activeConversation = conversations.find((c) => c.id === activeConversationId) || null;
  const messages = activeConversation?.messages ?? [];

  // Auto-scroll to bottom
  const scrollToBottom = useCallback(() => {
    requestAnimationFrame(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
    });
  }, []);

  useEffect(() => {
    if (messages.length > 0) {
      scrollToBottom();
    }
  }, [messages, scrollToBottom]);

  // Cleanup streaming timer on unmount
  useEffect(() => {
    return () => {
      if (streamTimerRef.current) {
        clearInterval(streamTimerRef.current);
      }
    };
  }, []);

  const updateConversation = useCallback((id: string, updater: (conv: Conversation) => Conversation) => {
    setConversations((prev) => prev.map((c) => (c.id === id ? updater(c) : c)));
  }, []);

  const updateMessage = useCallback((convId: string, msgId: string, updater: (msg: ChatMessage) => ChatMessage) => {
    setConversations((prev) =>
      prev.map((c) =>
        c.id === convId
          ? {
              ...c,
              messages: c.messages.map((m) => (m.id === msgId ? updater(m) : m)),
              updatedAt: Date.now(),
            }
          : c
      )
    );
  }, []);

  const handleNewChat = useCallback(() => {
    setActiveConversationId(null);
    setInputValue('');
    setSidebarOpen(false);
  }, []);

  const handleSelectConversation = useCallback((id: string) => {
    setActiveConversationId(id);
    setSidebarOpen(false);
  }, []);

  const handleDeleteConversation = useCallback((id: string) => {
    setConversations((prev) => prev.filter((c) => c.id !== id));
    if (activeConversationId === id) {
      setActiveConversationId(null);
    }
  }, [activeConversationId]);

  const handleSourceClick = useCallback((source: LegalSource) => {
    setDrawerSource(source);
    setDrawerOpen(true);
  }, []);

  const stopStreaming = useCallback(() => {
    streamingRef.current = false;
    if (streamTimerRef.current) {
      clearInterval(streamTimerRef.current);
      streamTimerRef.current = null;
    }
    setIsStreaming(false);
  }, []);

  const simulateResponse = useCallback(
    async (convId: string, assistantMsgId: string, query: string) => {
      const result = await getResponse(query);
      const { content, sources, ragSteps } = result;

      // Thinking phase
      updateMessage(convId, assistantMsgId, (msg) => ({
        ...msg,
        isThinking: true,
        isStreaming: true,
      }));

      // After thinking, start streaming the content
      setTimeout(() => {
        if (!streamingRef.current) return;

        updateMessage(convId, assistantMsgId, (msg) => ({
          ...msg,
          isThinking: false,
          content: '',
          sources: [],
          ragSteps: developerMode ? ragSteps : undefined,
        }));

        // Stream content word by word
        const words = content.split(' ');
        let wordIndex = 0;

        streamTimerRef.current = setInterval(() => {
          if (!streamingRef.current) {
            if (streamTimerRef.current) {
              clearInterval(streamTimerRef.current);
              streamTimerRef.current = null;
            }
            return;
          }

          if (wordIndex >= words.length) {
            // Finished streaming
            if (streamTimerRef.current) {
              clearInterval(streamTimerRef.current);
              streamTimerRef.current = null;
            }
            streamingRef.current = false;
            setIsStreaming(false);

            updateMessage(convId, assistantMsgId, (msg) => ({
              ...msg,
              isStreaming: false,
              sources,
              ragSteps: developerMode ? ragSteps : undefined,
            }));
            return;
          }

          // Stream a few words per tick for realistic speed
          const wordsPerTick = 3;
          const nextWords = words.slice(wordIndex, wordIndex + wordsPerTick);
          wordIndex += wordsPerTick;

          updateMessage(convId, assistantMsgId, (msg) => ({
            ...msg,
            content: msg.content + (wordIndex > wordsPerTick ? ' ' : '') + nextWords.join(' '),
          }));
        }, 40);
      }, 1200 + Math.random() * 800);
    },
    [updateMessage, developerMode]
  );

  const handleSubmit = useCallback(() => {
    const query = inputValue.trim();
    if (!query || isStreaming) return;

    setInputValue('');
    streamingRef.current = true;
    setIsStreaming(true);

    const userMsg: ChatMessage = {
      id: generateMessageId(),
      role: 'user',
      content: query,
      timestamp: Date.now(),
    };

    const assistantMsgId = generateMessageId();
    const assistantMsg: ChatMessage = {
      id: assistantMsgId,
      role: 'assistant',
      content: '',
      isThinking: true,
      isStreaming: true,
      timestamp: Date.now(),
    };

    if (!activeConversationId) {
      const convId = generateConversationId();
      const title = query.length > 50 ? query.slice(0, 50) + '...' : query;

      const newConv: Conversation = {
        id: convId,
        title,
        messages: [userMsg, assistantMsg],
        createdAt: Date.now(),
        updatedAt: Date.now(),
      };

      setConversations((prev) => [newConv, ...prev]);
      setActiveConversationId(convId);
      simulateResponse(convId, assistantMsgId, query);
    } else {
      updateConversation(activeConversationId, (conv) => ({
        ...conv,
        messages: [...conv.messages, userMsg, assistantMsg],
        updatedAt: Date.now(),
      }));
      simulateResponse(activeConversationId, assistantMsgId, query);
    }
  }, [inputValue, isStreaming, activeConversationId, updateConversation, simulateResponse]);

  const handleExampleClick = useCallback((question: string) => {
    setInputValue(question);
  }, []);

  const hasMessages = messages.length > 0;

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      {/* Sidebar */}
      <Sidebar
        conversations={conversations}
        activeConversationId={activeConversationId}
        onSelectConversation={handleSelectConversation}
        onNewChat={handleNewChat}
        onDeleteConversation={handleDeleteConversation}
        developerMode={developerMode}
        onToggleDeveloperMode={() => setDeveloperMode((v) => !v)}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      {/* Main content area */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* Top bar */}
        <header className="flex items-center justify-between px-3 sm:px-4 py-3 border-b border-border bg-card/50 backdrop-blur-sm z-10">
          <div className="flex items-center gap-2">
            {/* Mobile menu button */}
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden flex h-9 w-9 items-center justify-center rounded-lg hover:bg-muted transition-colors"
            >
              <Menu className="h-5 w-5 text-foreground" />
            </button>

            {/* Mobile brand */}
            <div className="lg:hidden flex items-center gap-2">
              <div className="flex h-7 w-7 items-center justify-center rounded-md bg-navy-900">
                <Scale className="h-4 w-4 text-uae-green-light" />
              </div>
              <span className="text-sm font-semibold text-foreground">UAE Legislation AI</span>
            </div>

            {/* Desktop conversation title */}
            {activeConversation && (
              <h2 className="hidden lg:block text-sm font-medium text-foreground truncate max-w-xs">
                {activeConversation.title}
              </h2>
            )}
          </div>

          {/* Right side actions */}
          <div className="flex items-center gap-2">
            {developerMode && (
              <span className="flex items-center gap-1.5 rounded-full bg-uae-green/10 px-2.5 py-1 text-xs font-medium text-uae-green-dark ring-1 ring-uae-green/20">
                <Code2 className="h-3 w-3" />
                Dev Mode
              </span>
            )}
          </div>
        </header>

        {/* Chat area */}
        <div
          ref={scrollContainerRef}
          className="flex-1 overflow-y-auto scrollbar-thin"
        >
          {hasMessages ? (
            <div className="py-4">
              {messages.map((message) => (
                <ChatMessageItem
                  key={message.id}
                  message={message}
                  showRagVisualization={developerMode}
                  onSourceClick={handleSourceClick}
                  onRetry={message.isError ? handleSubmit : undefined}
                />
              ))}
              <div ref={messagesEndRef} className="h-4" />
            </div>
          ) : (
            <WelcomeScreen onQuestionClick={handleExampleClick} examples={EXAMPLE_QUESTIONS} />
          )}
        </div>

        {/* Input */}
        <ChatInput
          value={inputValue}
          onChange={setInputValue}
          onSubmit={handleSubmit}
          disabled={isStreaming}
          isStreaming={isStreaming}
          onStop={stopStreaming}
        />
      </div>

      {/* Document Drawer */}
      <DocumentDrawer
        source={drawerSource}
        open={drawerOpen}
        onOpenChange={setDrawerOpen}
      />
    </div>
  );
}

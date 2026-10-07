import { useState, useMemo } from 'react';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import type { Conversation } from '@/types';
import {
  Scale,
  Plus,
  Search,
  MessageSquare,
  Trash2,
  Code2,
  X,
  Building2,
  Users,
  TrendingUp,
  Receipt,
  HelpCircle,
} from 'lucide-react';

interface SidebarProps {
  conversations: Conversation[];
  activeConversationId: string | null;
  onSelectConversation: (id: string) => void;
  onNewChat: () => void;
  onDeleteConversation: (id: string) => void;
  developerMode: boolean;
  onToggleDeveloperMode: () => void;
  isOpen: boolean;
  onClose: () => void;
}

const ICON_MAP: Record<string, React.ElementType> = {
  Building2,
  Users,
  TrendingUp,
  Receipt,
  HelpCircle,
};

function formatTimeAgo(timestamp: number): string {
  const diff = Date.now() - timestamp;
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);
  if (minutes < 1) return 'Just now';
  if (minutes < 60) return `${minutes}m ago`;
  if (hours < 24) return `${hours}h ago`;
  if (days < 7) return `${days}d ago`;
  return new Date(timestamp).toLocaleDateString();
}

function groupConversations(conversations: Conversation[]): { label: string; items: Conversation[] }[] {
  const now = Date.now();
  const today: Conversation[] = [];
  const yesterday: Conversation[] = [];
  const earlier: Conversation[] = [];

  const sorted = [...conversations].sort((a, b) => b.updatedAt - a.updatedAt);

  for (const conv of sorted) {
    const dayDiff = Math.floor((now - conv.updatedAt) / 86400000);
    if (dayDiff < 1) today.push(conv);
    else if (dayDiff < 2) yesterday.push(conv);
    else earlier.push(conv);
  }

  const groups: { label: string; items: Conversation[] }[] = [];
  if (today.length) groups.push({ label: 'Today', items: today });
  if (yesterday.length) groups.push({ label: 'Yesterday', items: yesterday });
  if (earlier.length) groups.push({ label: 'Earlier', items: earlier });
  return groups;
}

export function Sidebar({
  conversations,
  activeConversationId,
  onSelectConversation,
  onNewChat,
  onDeleteConversation,
  developerMode,
  onToggleDeveloperMode,
  isOpen,
  onClose,
}: SidebarProps) {
  const [searchQuery, setSearchQuery] = useState('');

  const filtered = useMemo(() => {
    if (!searchQuery.trim()) return conversations;
    const q = searchQuery.toLowerCase();
    return conversations.filter((c) =>
      c.title.toLowerCase().includes(q) ||
      c.messages.some((m) => m.content.toLowerCase().includes(q))
    );
  }, [conversations, searchQuery]);

  const groups = groupConversations(filtered);

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-navy-950/40 backdrop-blur-sm lg:hidden animate-fade-in"
          onClick={onClose}
        />
      )}

      <aside
        className={cn(
          'fixed lg:relative z-50 h-full w-[280px] flex flex-col bg-card border-r border-border transition-transform duration-300 ease-in-out lg:translate-x-0',
          isOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        {/* Branding */}
        <div className="flex items-center justify-between px-5 pt-5 pb-4">
          <div className="flex items-center gap-2.5">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-uae-green/10 ring-1 ring-uae-green/25">
              <Scale className="h-5 w-5 text-uae-green" />
            </div>
            <div>
              <h1 className="text-sm font-semibold leading-tight text-foreground">UAE Legislation AI</h1>
              <p className="text-[11px] text-muted-foreground leading-tight">Legal Research Platform</p>
            </div>
          </div>
          <Button
            variant="ghost"
            size="icon"
            className="h-8 w-8 text-muted-foreground hover:bg-muted hover:text-foreground lg:hidden"
            onClick={onClose}
          >
            <X className="h-4 w-4" />
          </Button>
        </div>

        {/* New Chat */}
        <div className="px-3 pb-3">
          <Button
            onClick={onNewChat}
            className="w-full justify-start gap-2 bg-uae-green text-white hover:bg-uae-green-dark font-medium shadow-sm"
          >
            <Plus className="h-4 w-4" />
            New Chat
          </Button>
        </div>

        {/* Search */}
        <div className="px-3 pb-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground/60" />
            <input
              type="text"
              placeholder="Search conversations..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full h-9 rounded-lg bg-muted/60 border border-border pl-9 pr-3 text-sm text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:ring-2 focus:ring-uae-green/15 focus:border-uae-green/30 focus:bg-card transition-all"
            />
          </div>
        </div>

        {/* Conversations list */}
        <ScrollArea className="flex-1 px-3 scrollbar-thin">
          {filtered.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 px-4 text-center">
              <MessageSquare className="h-8 w-8 text-muted-foreground/25 mb-2" />
              <p className="text-xs text-muted-foreground/70">
                {searchQuery ? 'No conversations found' : 'No conversations yet'}
              </p>
            </div>
          ) : (
            <div className="space-y-4 pb-4">
              {groups.map((group) => (
                <div key={group.label}>
                  <p className="text-[11px] font-medium text-muted-foreground/50 uppercase tracking-wider px-2 mb-1.5">
                    {group.label}
                  </p>
                  <div className="space-y-0.5">
                    {group.items.map((conv) => {
                      const lastMessage = conv.messages[conv.messages.length - 1];
                      const icon = conv.messages[0]?.content
                        ? detectCategoryIcon(conv.messages[0].content)
                        : 'HelpCircle';
                      const Icon = ICON_MAP[icon] || MessageSquare;

                      return (
                        <div
                          key={conv.id}
                          className={cn(
                            'group flex items-center gap-2.5 rounded-lg px-2.5 py-2 cursor-pointer transition-all',
                            activeConversationId === conv.id
                              ? 'bg-uae-green/8 text-foreground ring-1 ring-uae-green/15'
                              : 'text-foreground/80 hover:bg-muted/70'
                          )}
                          onClick={() => onSelectConversation(conv.id)}
                        >
                          <Icon className={cn(
                            'h-4 w-4 shrink-0 transition-colors',
                            activeConversationId === conv.id ? 'text-uae-green' : 'text-muted-foreground/60'
                          )} />
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium truncate leading-tight">{conv.title}</p>
                            <p className="text-[11px] text-muted-foreground/60 truncate mt-0.5">
                              {lastMessage ? formatTimeAgo(conv.updatedAt) : 'Empty'}
                            </p>
                          </div>
                          <Button
                            variant="ghost"
                            size="icon"
                            className="h-6 w-6 opacity-0 group-hover:opacity-100 text-muted-foreground hover:bg-muted hover:text-destructive transition-all"
                            onClick={(e) => {
                              e.stopPropagation();
                              onDeleteConversation(conv.id);
                            }}
                          >
                            <Trash2 className="h-3 w-3" />
                          </Button>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          )}
        </ScrollArea>

        {/* Footer — Developer Mode toggle */}
        <div className="border-t border-border p-3">
          <button
            onClick={onToggleDeveloperMode}
            className={cn(
              'flex w-full items-center justify-between rounded-lg px-3 py-2.5 text-sm transition-all',
              developerMode
                ? 'bg-uae-green/10 text-uae-green-dark ring-1 ring-uae-green/20'
                : 'text-foreground/80 hover:bg-muted/70'
            )}
          >
            <span className="flex items-center gap-2 font-medium">
              <Code2 className={cn('h-4 w-4', developerMode ? 'text-uae-green' : 'text-muted-foreground')} />
              Developer Mode
            </span>
            <span
              className={cn(
                'relative h-5 w-9 rounded-full transition-colors',
                developerMode ? 'bg-uae-green' : 'bg-muted-foreground/25'
              )}
            >
              <span
                className={cn(
                  'absolute top-0.5 h-4 w-4 rounded-full bg-white shadow-sm transition-transform',
                  developerMode ? 'translate-x-4' : 'translate-x-0.5'
                )}
              />
            </span>
          </button>
        </div>
      </aside>
    </>
  );
}

function detectCategoryIcon(text: string): string {
  const lower = text.toLowerCase();
  if (lower.includes('company') || lower.includes('free zone') || lower.includes('business')) return 'Building2';
  if (lower.includes('labor') || lower.includes('employee') || lower.includes('worker') || lower.includes('gratuity')) return 'Users';
  if (lower.includes('invest') || lower.includes('fdi') || lower.includes('foreign')) return 'TrendingUp';
  if (lower.includes('vat') || lower.includes('tax')) return 'Receipt';
  return 'HelpCircle';
}

import { Pin, Plus, MessageSquare } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAssistantStore } from "@/stores/assistant.store";
import { formatRelativeTime } from "@/utils/format";
import { cn } from "@/utils/cn";

export function ConversationSidebar() {
  const { conversations, activeConversationId, startNewConversation, setActiveConversation, togglePinned } =
    useAssistantStore();

  const sorted = [...conversations].sort((a, b) => {
    if (a.pinned !== b.pinned) return a.pinned ? -1 : 1;
    return new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime();
  });

  return (
    <div className="flex h-full w-64 shrink-0 flex-col border-r border-border">
      <div className="p-3">
        <Button className="w-full" size="sm" onClick={() => startNewConversation()}>
          <Plus className="h-4 w-4" /> New conversation
        </Button>
      </div>
      <div className="flex-1 space-y-0.5 overflow-y-auto px-2 pb-3 scrollbar-thin">
        {sorted.length === 0 ? (
          <p className="px-2 py-6 text-center text-xs text-muted-foreground">No conversations yet.</p>
        ) : (
          sorted.map((c) => (
            <button
              key={c.id}
              onClick={() => setActiveConversation(c.id)}
              className={cn(
                "group flex w-full items-start gap-2 rounded-lg px-2.5 py-2 text-left text-sm transition-colors",
                c.id === activeConversationId ? "bg-accent text-accent-foreground" : "hover:bg-muted"
              )}
            >
              <MessageSquare className="mt-0.5 h-3.5 w-3.5 shrink-0 text-muted-foreground" />
              <span className="min-w-0 flex-1">
                <span className="block truncate font-medium">{c.title}</span>
                <span className="block truncate text-xs text-muted-foreground">
                  {formatRelativeTime(c.updatedAt)}
                </span>
              </span>
              <span
                role="button"
                onClick={(e) => {
                  e.stopPropagation();
                  togglePinned(c.id);
                }}
                className={cn(
                  "shrink-0 opacity-0 transition-opacity group-hover:opacity-100",
                  c.pinned && "opacity-100 text-primary"
                )}
              >
                <Pin className="h-3.5 w-3.5" />
              </span>
            </button>
          ))
        )}
      </div>
    </div>
  );
}

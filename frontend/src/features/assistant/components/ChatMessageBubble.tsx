import { AlertCircle, Sparkles } from "lucide-react";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { MarkdownRenderer } from "@/features/assistant/components/MarkdownRenderer";
import { ExecutionTimeline } from "@/features/assistant/components/ExecutionTimeline";
import { SourcesPanel } from "@/features/assistant/components/SourcesPanel";
import { RecommendationsList } from "@/features/assistant/components/RecommendationsList";
import { useAuthStore } from "@/stores/auth.store";
import { initials, formatDateTime } from "@/utils/format";
import type { ChatMessage } from "@/types/domain";
import { cn } from "@/utils/cn";

export function ChatMessageBubble({ message }: { message: ChatMessage }) {
  const fullName = useAuthStore((s) => s.fullName);
  const isUser = message.role === "user";

  return (
    <div className={cn("flex gap-3", isUser && "flex-row-reverse")}>
      <Avatar className="mt-0.5 h-8 w-8 shrink-0">
        <AvatarFallback className={cn(!isUser && "bg-primary text-primary-foreground")}>
          {isUser ? initials(fullName ?? "You") : <Sparkles className="h-3.5 w-3.5" />}
        </AvatarFallback>
      </Avatar>

      <div className={cn("flex max-w-[85%] flex-col gap-1.5", isUser && "items-end")}>
        <div
          className={cn(
            "rounded-2xl px-4 py-3 text-sm shadow-soft",
            isUser ? "bg-primary text-primary-foreground" : "border border-border bg-card"
          )}
        >
          {isUser ? (
            <p className="whitespace-pre-wrap">{message.content}</p>
          ) : message.error ? (
            <p className="flex items-center gap-1.5 text-destructive">
              <AlertCircle className="h-4 w-4" /> {message.error}
            </p>
          ) : (
            <>
              {message.executionEvents && message.executionEvents.length > 0 && (
                <div className="mb-3">
                  <ExecutionTimeline events={message.executionEvents} isActive={Boolean(message.streaming)} />
                </div>
              )}
              {message.content && <MarkdownRenderer content={message.content} />}
              {message.streaming && !message.content && (!message.executionEvents || message.executionEvents.length === 0) && (
                <span className="inline-flex items-center gap-1 text-muted-foreground">
                  <span className="h-1.5 w-1.5 animate-pulse-soft rounded-full bg-current" />
                  <span className="h-1.5 w-1.5 animate-pulse-soft rounded-full bg-current [animation-delay:0.15s]" />
                  <span className="h-1.5 w-1.5 animate-pulse-soft rounded-full bg-current [animation-delay:0.3s]" />
                </span>
              )}
              {message.response?.sources && <SourcesPanel sources={message.response.sources} />}
              {message.response?.recommendations && (
                <RecommendationsList recommendations={message.response.recommendations} />
              )}
              {message.response?.agent && (
                <Badge variant="outline" className="mt-3">
                  Answered by {message.response.agent}
                </Badge>
              )}
            </>
          )}
        </div>
        <span className="px-1 text-[11px] text-muted-foreground">{formatDateTime(message.createdAt)}</span>
      </div>
    </div>
  );
}

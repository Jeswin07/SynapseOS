import {
  AlertCircle,
  Bot,
  User,
} from "lucide-react";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";

import { MarkdownRenderer } from "@/features/assistant/components/MarkdownRenderer";
import { ExecutionTimeline } from "@/features/assistant/components/ExecutionTimeline";
import { SourcesPanel } from "@/features/assistant/components/SourcesPanel";
import { RecommendationsList } from "@/features/assistant/components/RecommendationsList";

import { useAuthStore } from "@/stores/auth.store";

import { formatDateTime } from "@/utils/format";
import { cn } from "@/utils/cn";

import type { ChatMessage } from "@/types/domain";

export function ChatMessageBubble({
  message,
}: {
  message: ChatMessage;
}) {
  const fullName = useAuthStore(
    (s) => s.fullName
  );

  const isUser =
    message.role === "user";

  return (
    <div
      className={cn(
        "flex gap-4",
        isUser && "flex-row-reverse"
      )}
    >
      <Avatar className="mt-1 h-10 w-10 shrink-0 border">

        <AvatarFallback
          className={cn(
            isUser
              ? "bg-primary text-primary-foreground"
              : "bg-muted"
          )}
        >
          {isUser ? (
            <User className="h-4 w-4" />
          ) : (
            <Bot className="h-4 w-4" />
          )}
        </AvatarFallback>

      </Avatar>

      <div
        className={cn(
          "flex max-w-[82%] flex-col",
          isUser && "items-end"
        )}
      >
        {/* Header */}

        <div
          className={cn(
            "mb-1 flex items-center gap-2 text-xs text-muted-foreground",
            isUser &&
              "flex-row-reverse"
          )}
        >
          <span className="font-medium text-foreground">
            {isUser
              ? fullName ?? "You"
              : "SynapseOS"}
          </span>

          <span>
            {formatDateTime(
              message.createdAt
            )}
          </span>
        </div>

        {/* Bubble */}

        <div
          className={cn(
            "rounded-xl border px-4 py-3 shadow-sm text-sm",
            isUser
              ? "border-primary bg-primary text-primary-foreground"
              : "border-border bg-card"
          )}
        >
          {isUser ? (
            <p className="whitespace-pre-wrap leading-relaxed">
              {message.content}
            </p>
          ) : message.error ? (
            <div className="flex items-center gap-2 text-destructive">
              <AlertCircle className="h-5 w-5" />
              <span>{message.error}</span>
            </div>
          ) : (
            <>
              {/* Timeline */}

              {message.executionEvents &&
                message.executionEvents
                  .length > 0 && (
                  <div className="mb-3">
                    <ExecutionTimeline
                      events={
                        message.executionEvents
                      }
                      isActive={Boolean(
                        message.streaming
                      )}
                    />
                  </div>
                )}

              {/* Markdown */}
              {message.content && (
                  <MarkdownRenderer
                      content={message.content}
                  />

              )}

              {/* Streaming */}

              {message.streaming &&
                !message.content && (
                  <div className="flex items-center gap-2 py-2">

                    <div className="h-2 w-2 animate-pulse rounded-full bg-primary" />

                    <div className="h-2 w-2 animate-pulse rounded-full bg-primary delay-100" />

                    <div className="h-2 w-2 animate-pulse rounded-full bg-primary delay-200" />

                    <span className="ml-2 text-sm text-muted-foreground">
                      Thinking...
                    </span>

                  </div>
                )}

              {/* Sources */}

              {message.response
                ?.sources &&
                message.response
                  .sources.length >
                  0 && (
                  <div className="mt-4">
                    <SourcesPanel
                      sources={
                        message.response
                          .sources
                      }
                    />
                  </div>
                )}

              {/* Recommendations */}

              {message.response
                ?.recommendations &&
                message.response
                  .recommendations
                  .length > 0 && (
                  <div className="mt-6">
                    <RecommendationsList
                      recommendations={
                        message.response
                          .recommendations
                      }
                    />
                  </div>
                )}

              {/* Footer */}

              <div className="mt-5 flex items-center justify-between">

                {message.response
                  ?.agent && (
                  <Badge
                    variant="secondary"
                  >
                    {
                      message.response
                        .agent
                    }
                  </Badge>
                )}

                {message.streaming && (
                  <Badge
                    variant="outline"
                  >
                    Streaming
                  </Badge>
                )}

              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
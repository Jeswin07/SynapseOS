import {
  MessageSquare,
  Plus,
  Pin,
  Search,
} from "lucide-react";
import { useMemo, useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import { useAssistantStore } from "@/stores/assistant.store";

import { formatRelativeTime } from "@/utils/format";
import { cn } from "@/utils/cn";

import { CreateConversationDialog } from "./CreateConversationDialog";

export function ConversationSidebar() {
  const {
    conversations,
    activeConversationId,
    setActiveConversation,
    togglePinned,
  } = useAssistantStore();

  const [search, setSearch] = useState("");

  const [dialogOpen, setDialogOpen] =
    useState(false);

  const filtered = useMemo(() => {
    const sorted = [...conversations].sort((a, b) => {
      if (a.pinned !== b.pinned) {
        return a.pinned ? -1 : 1;
      }

      return (
        new Date(b.updatedAt).getTime() -
        new Date(a.updatedAt).getTime()
      );
    });

    if (!search.trim()) {
      return sorted;
    }

    return sorted.filter((conversation) =>
      conversation.title
        .toLowerCase()
        .includes(search.toLowerCase())
    );
  }, [conversations, search]);

  return (
    <>
      <CreateConversationDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
      />

      <aside className="flex h-full w-72 shrink-0 flex-col border-r bg-background">

        {/* Header */}

        <div className="border-b px-4 py-4">

          <h2 className="text-lg font-semibold">
            SynapseOS
          </h2>

          <p className="mt-1 text-xs text-muted-foreground">
            Enterprise AI Assistant
          </p>

          <Button
            className="mt-4 w-full justify-start"
            onClick={() => setDialogOpen(true)}
          >
            <Plus className="mr-2 h-4 w-4" />
            New Conversation
          </Button>

        </div>

        {/* Search */}

        <div className="border-b p-3">

          <div className="relative">

            <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />

            <Input
              placeholder="Search conversations..."
              value={search}
              onChange={(e) =>
                setSearch(e.target.value)
              }
              className="pl-9"
            />

          </div>

        </div>

        {/* Conversation List Starts Here */}
        <div className="flex-1 overflow-y-auto px-2 py-2">
          {filtered.length === 0 ? (
            <div className="px-3 py-8 text-center text-sm text-muted-foreground">
              No conversations found.
            </div>
          ) : (
            filtered.map((conversation) => {
              const active =
                conversation.id === activeConversationId;

              return (
                <button
                  key={conversation.id}
                  onClick={() =>
                    setActiveConversation(conversation.id)
                  }
                  className={cn(
                    "group mb-1 flex w-full items-start gap-3 rounded-xl p-3 text-left transition-all",
                    active
                      ? "bg-primary text-primary-foreground shadow-sm"
                      : "hover:bg-muted"
                  )}
                >
                  <MessageSquare
                    className={cn(
                      "mt-0.5 h-4 w-4 shrink-0",
                      active
                        ? "text-primary-foreground"
                        : "text-muted-foreground"
                    )}
                  />

                  <div className="min-w-0 flex-1">
                    <div className="truncate font-medium">
                      {conversation.title}
                    </div>

                    <div
                      className={cn(
                        "mt-1 text-xs",
                        active
                          ? "text-primary-foreground/80"
                          : "text-muted-foreground"
                      )}
                    >
                      {formatRelativeTime(
                        conversation.updatedAt
                      )}
                    </div>
                  </div>

                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      togglePinned(conversation.id);
                    }}
                    className={cn(
                      "opacity-0 transition group-hover:opacity-100",
                      conversation.pinned &&
                        "opacity-100"
                    )}
                  >
                    <Pin
                      className={cn(
                        "h-4 w-4",
                        conversation.pinned &&
                          "fill-current"
                      )}
                    />
                  </button>
                </button>
              );
            })
          )}
        </div>

        {/* Footer */}

        <div className="border-t px-4 py-3">
          <div className="text-xs text-muted-foreground">
            {conversations.length} conversation
            {conversations.length !== 1 && "s"}
          </div>
        </div>

      </aside>
    </>
  );
}
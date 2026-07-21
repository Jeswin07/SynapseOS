import { useEffect, useRef } from "react";
import { Sparkles } from "lucide-react";

import { ConversationSidebar } from "@/features/assistant/components/ConversationSidebar";
import { ChatComposer } from "@/features/assistant/components/ChatComposer";
import { ChatMessageBubble } from "@/features/assistant/components/ChatMessageBubble";

import { useAssistantStore } from "@/stores/assistant.store";
import { useAssistantChat } from "@/hooks/useAssistant";

export default function AssistantPage() {
  const {
    conversations,
    activeConversationId,
    streamingMode,
    setStreamingMode,
  } = useAssistantStore();

  const { sendMessage, isSending, cancel } =
    useAssistantChat();

  const scrollRef =
    useRef<HTMLDivElement>(null);

  const conversation = conversations.find(
    (c) => c.id === activeConversationId
  );

  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [conversation?.messages]);

  function handleSend(text: string) {
    if (!conversation) {
      alert(
        "Create a conversation before chatting."
      );
      return;
    }

    sendMessage(
      conversation.id,
      text,
      streamingMode
    );
  }

  return (
    <div className="-m-4 flex h-[calc(100vh-3.5rem)] overflow-hidden sm:-m-6">

      <ConversationSidebar />

      <div className="flex min-w-0 flex-1 flex-col">
        {/* Header */}

        <div className="border-b border-border bg-background/80 backdrop-blur">
          <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-3">

            <div>
              <p className="text-xs uppercase tracking-wide text-muted-foreground">
                Active Conversation
              </p>

              <p className="font-medium">
                {conversation?.title ?? "No Conversation Selected"}
              </p>
            </div>

            <div className="text-right">
              <p className="text-xs uppercase tracking-wide text-muted-foreground">
                AI Assistant
              </p>

              <p className="font-medium">
                Business Agent
              </p>
            </div>

          </div>
        </div>

        {/* Chat */}

        <div
          ref={scrollRef}
          className="flex-1 overflow-y-auto scrollbar-thin"
        >
          <div className="mx-auto max-w-5xl space-y-8 px-4 py-6 sm:px-6">

            {(!conversation ||
              conversation.messages.length === 0) && (

              <div className="flex flex-col items-center justify-center gap-3 py-24 text-center">

                <div className="rounded-2xl bg-primary/10 p-4 text-primary">
                  <Sparkles className="h-7 w-7" />
                </div>

                <h2 className="text-xl font-semibold">
                  Enterprise Decision Intelligence
                </h2>

                <p className="max-w-xl text-sm text-muted-foreground">
                  Create a conversation from the sidebar and choose the
                  dataset version that conversation should use. Once created,
                  simply ask questions about forecasting, prediction, risk,
                  analytics, enterprise knowledge, or business strategy.
                </p>

              </div>

            )}

            {conversation?.messages.map((message) => (
              <ChatMessageBubble
                key={message.id}
                message={message}
              />
            ))}

          </div>
        </div>

        {/* Composer */}

        <div className="mx-auto w-full max-w-5xl px-4 pb-4 sm:px-6">

          <ChatComposer
            onSend={handleSend}
            isSending={isSending}
            onCancel={cancel}
            streamingMode={streamingMode}
            onToggleStreaming={setStreamingMode}
          />

        </div>

      </div>

    </div>
  );
}
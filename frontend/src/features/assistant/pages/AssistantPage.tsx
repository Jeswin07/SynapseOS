import { useEffect, useRef, useState } from "react";
import { Sparkles } from "lucide-react";

import { ConversationSidebar } from "@/features/assistant/components/ConversationSidebar";
import { ChatMessageBubble } from "@/features/assistant/components/ChatMessageBubble";
import { ChatComposer } from "@/features/assistant/components/ChatComposer";

import { DatasetVersionSelect } from "@/components/common/DatasetVersionSelect";
import { Card, CardContent } from "@/components/ui/card";

import { useAssistantStore } from "@/stores/assistant.store";
import { useAssistantChat } from "@/hooks/useAssistant";

export default function AssistantPage() {
  const {
    conversations,
    activeConversationId,
    ensureActiveConversation,
    streamingMode,
    setStreamingMode,
  } = useAssistantStore();

  const { sendMessage, isSending, cancel } = useAssistantChat();

  const scrollRef = useRef<HTMLDivElement>(null);

  const [datasetId, setDatasetId] = useState<string | null>(null);
  const [versionId, setVersionId] = useState<string | null>(null);

  useEffect(() => {
    ensureActiveConversation();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

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
    if (!versionId) {
      alert("Please select a dataset version first.");
      return;
    }

    const id = ensureActiveConversation();

    sendMessage(
      id,
      text,
      streamingMode,
      versionId,
    );
  }

  return (
    <div className="-m-4 flex h-[calc(100vh-3.5rem)] overflow-hidden sm:-m-6">
      <ConversationSidebar />

      <div className="flex min-w-0 flex-1 flex-col">

        {/* Dataset Selection */}

        <div className="mx-auto w-full max-w-3xl px-4 pt-4 sm:px-6">

          <Card>

            <CardContent className="p-5">

              <DatasetVersionSelect
                datasetId={datasetId}
                versionId={versionId}
                onDatasetChange={(id) => {
                  setDatasetId(id);
                  setVersionId(null);
                }}
                onVersionChange={setVersionId}
              />

            </CardContent>

          </Card>

        </div>

        {/* Chat */}

        <div
          ref={scrollRef}
          className="flex-1 overflow-y-auto scrollbar-thin"
        >
          <div className="mx-auto max-w-3xl space-y-6 px-4 py-6 sm:px-6">

            {(!conversation ||
              conversation.messages.length === 0) && (

              <div className="flex flex-col items-center justify-center gap-3 py-24 text-center">

                <div className="rounded-2xl bg-primary/10 p-4 text-primary">
                  <Sparkles className="h-7 w-7" />
                </div>

                <h2 className="text-xl font-semibold">
                  How can I help with your business today?
                </h2>

                <p className="max-w-md text-sm text-muted-foreground">
                  Select a dataset version above, then ask questions about
                  analytics, forecasting, prediction, risk analysis,
                  scenario planning, or your enterprise knowledge base.
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

        <div className="mx-auto w-full max-w-3xl px-4 pb-4 sm:px-6">

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
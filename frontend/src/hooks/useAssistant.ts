import { useCallback, useRef, useState } from "react";
import { assistantService } from "@/services/assistant.service";
import { useAssistantStore } from "@/stores/assistant.store";
import type { ChatMessage } from "@/types/domain";
import type { StreamEvent } from "@/types/api";

export function useAssistantChat() {
  const [isSending, setIsSending] = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  const {
    appendMessage,
    updateMessage,
    renameFromFirstMessage,
  } = useAssistantStore();

  const sendMessage = useCallback(
    async (
      conversationId: string,
      text: string,
      streaming: boolean,
    ) => {
      const userMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: "user",
        content: text,
        createdAt: new Date().toISOString(),
      };

      appendMessage(conversationId, userMessage);
      renameFromFirstMessage(conversationId, text);

      const assistantMessageId = crypto.randomUUID();

      const initialEvents: StreamEvent[] = [
        {
          type: "status",
          message: "Planning request...",
          agent: null,
          data: {},
        },
      ];

      const assistantMessage: ChatMessage = {
        id: assistantMessageId,
        role: "assistant",
        content: "",
        createdAt: new Date().toISOString(),
        streaming: true,
        executionEvents: initialEvents,
      };

      appendMessage(conversationId, assistantMessage);
      setIsSending(true);

      if (streaming) {
        const controller = new AbortController();
        abortRef.current = controller;

        const events: StreamEvent[] = [...initialEvents];

        await assistantService.streamChat(
          {
            conversation_id: conversationId,
            message: text,
            metadata: {
            },
          },
          {
            onEvent: (event) => {
              if (
                event.type === "status" &&
                event.message.toLowerCase().includes("planning")
              ) {
                events[0] = event;
              } else {
                events.push(event);
              }

              updateMessage(conversationId, assistantMessageId, {
                executionEvents: [...events],
                content:
                  event.type === "status"
                    ? event.message
                    : "",
              });
            },

            onFinal: (response) => {
              updateMessage(conversationId, assistantMessageId, {
                content: response.answer,
                response,
                executionEvents: [...events],
                streaming: false,
              });

              setIsSending(false);
            },

            onError: (message) => {
              updateMessage(conversationId, assistantMessageId, {
                streaming: false,
                error: message,
              });

              setIsSending(false);
            },
          },
          controller.signal,
        );

        setIsSending(false);
      } else {
        try {
          const response = await assistantService.chat({
            conversation_id: conversationId,
            message: text,
            metadata: {
            },
          });

          updateMessage(conversationId, assistantMessageId, {
            content: response.answer,
            response,
            streaming: false,
          });
        } catch (err) {
          updateMessage(conversationId, assistantMessageId, {
            streaming: false,
            error:
              err instanceof Error
                ? err.message
                : "The assistant could not respond. Please try again.",
          });
        } finally {
          setIsSending(false);
        }
      }
    },
    [
      appendMessage,
      updateMessage,
      renameFromFirstMessage,
    ],
  );

  const cancel = useCallback(() => {
    abortRef.current?.abort();
    setIsSending(false);
  }, []);

  return {
    sendMessage,
    isSending,
    cancel,
  };
}
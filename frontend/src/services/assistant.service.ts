import { apiClient, API_BASE_URL } from "@/services/apiClient";
import { useAuthStore } from "@/stores/auth.store";
import type { AssistantChatRequest, AssistantChatResponse, StreamEvent } from "@/types/api";

export const assistantService = {
  chat(payload: AssistantChatRequest) {
    return apiClient.post<AssistantChatResponse>("/assistant/chat", payload).then((r) => r.data);
  },

  /**
   * Streams Server-Sent Events from POST /assistant/chat/stream.
   * The endpoint uses SSE over a POST body, so we use fetch() with a
   * ReadableStream reader rather than EventSource (which only supports GET).
   *
   * Emits StreamEvent objects for progress, then a final callback with the
   * completed AssistantChatResponse once the backend sends {type:"final",...}.
   */
  async streamChat(
    payload: AssistantChatRequest,
    handlers: {
      onEvent: (event: StreamEvent) => void;
      onFinal: (response: AssistantChatResponse) => void;
      onError: (message: string) => void;
    },
    signal?: AbortSignal
  ) {
    const token = useAuthStore.getState().accessToken;

    try {
      const res = await fetch(`${API_BASE_URL}/assistant/chat/stream`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "text/event-stream",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify(payload),
        signal,
      });

      if (!res.ok || !res.body) {
        handlers.onError(`Assistant stream failed (status ${res.status}).`);
        return;
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const chunks = buffer.split("\n\n");
        buffer = chunks.pop() ?? "";

        for (const chunk of chunks) {
          const line = chunk.trim();
          if (!line.startsWith("data:")) continue;
          const jsonStr = line.slice(5).trim();
          if (!jsonStr) continue;

          try {
            const parsed = JSON.parse(jsonStr);
            if (parsed.type === "final") {
              handlers.onFinal(parsed.response as AssistantChatResponse);
            } else {
              handlers.onEvent(parsed as StreamEvent);
            }
          } catch {
            // Ignore malformed SSE frames rather than crashing the stream.
          }
        }
      }
    } catch (err) {
      if ((err as Error).name === "AbortError") return;
      handlers.onError("Lost connection to the assistant. Please try again.");
    }
  },
};

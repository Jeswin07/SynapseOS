import { create } from "zustand";
import type { Conversation, ChatMessage } from "@/types/domain";

function newConversation(): Conversation {
  return {
    id: crypto.randomUUID(),
    title: "New conversation",
    pinned: false,
    updatedAt: new Date().toISOString(),
    messages: [],
  };
}

interface AssistantState {
  conversations: Conversation[];
  activeConversationId: string | null;
  streamingMode: boolean;
  startNewConversation: () => string;
  ensureActiveConversation: () => string;
  setActiveConversation: (id: string) => void;
  togglePinned: (id: string) => void;
  setStreamingMode: (value: boolean) => void;
  appendMessage: (conversationId: string, message: ChatMessage) => void;
  updateMessage: (conversationId: string, messageId: string, patch: Partial<ChatMessage>) => void;
  renameFromFirstMessage: (conversationId: string, text: string) => void;
}

export const useAssistantStore = create<AssistantState>((set, get) => ({
  conversations: [],
  activeConversationId: null,
  streamingMode: true,
  startNewConversation: () => {
    const conv = newConversation();
    set({ conversations: [conv, ...get().conversations], activeConversationId: conv.id });
    return conv.id;
  },
  ensureActiveConversation: () => {
    const { activeConversationId, conversations } = get();
    if (activeConversationId && conversations.some((c) => c.id === activeConversationId)) {
      return activeConversationId;
    }
    return get().startNewConversation();
  },
  setActiveConversation: (id) => set({ activeConversationId: id }),
  togglePinned: (id) =>
    set({
      conversations: get().conversations.map((c) => (c.id === id ? { ...c, pinned: !c.pinned } : c)),
    }),
  setStreamingMode: (value) => set({ streamingMode: value }),
  appendMessage: (conversationId, message) =>
    set({
      conversations: get().conversations.map((c) =>
        c.id === conversationId
          ? { ...c, messages: [...c.messages, message], updatedAt: new Date().toISOString() }
          : c
      ),
    }),
  updateMessage: (conversationId, messageId, patch) =>
    set({
      conversations: get().conversations.map((c) =>
        c.id === conversationId
          ? {
              ...c,
              messages: c.messages.map((m) => (m.id === messageId ? { ...m, ...patch } : m)),
              updatedAt: new Date().toISOString(),
            }
          : c
      ),
    }),
  renameFromFirstMessage: (conversationId, text) =>
    set({
      conversations: get().conversations.map((c) =>
        c.id === conversationId && c.title === "New conversation"
          ? { ...c, title: text.slice(0, 48) }
          : c
      ),
    }),
}));

import { create } from "zustand";
import type { Conversation, ChatMessage } from "@/types/domain";

interface AssistantState {
  conversations: Conversation[];
  activeConversationId: string | null;
  streamingMode: boolean;

  setConversations: (items: Conversation[]) => void;
  addConversation: (conversation: Conversation) => void;
  removeConversation: (id: string) => void;

  setActiveConversation: (id: string | null) => void;

  togglePinned: (id: string) => void;

  setStreamingMode: (value: boolean) => void;

  appendMessage: (
    conversationId: string,
    message: ChatMessage
  ) => void;

  updateMessage: (
    conversationId: string,
    messageId: string,
    patch: Partial<ChatMessage>
  ) => void;

  renameConversation: (
    conversationId: string,
    title: string
  ) => void;

  renameFromFirstMessage: (
    conversationId: string,
    text: string
  ) => void;
}

export const useAssistantStore =
create<AssistantState>((set, get) => ({

  conversations: [],

  activeConversationId: null,

  streamingMode: true,

  setConversations: (items) =>
    set({
      conversations: items,
    }),

  addConversation: (conversation) =>
    set({
      conversations: [
        conversation,
        ...get().conversations,
      ],
      activeConversationId: conversation.id,
    }),

  removeConversation: (id) =>
    set({
      conversations: get().conversations.filter(
        (c) => c.id !== id
      ),

      activeConversationId:
        get().activeConversationId === id
          ? null
          : get().activeConversationId,
    }),

  setActiveConversation: (id) =>
    set({
      activeConversationId: id,
    }),

  togglePinned: (id) =>
    set({
      conversations: get().conversations.map((c) =>
        c.id === id
          ? {
              ...c,
              pinned: !c.pinned,
            }
          : c
      ),
    }),

  setStreamingMode: (value) =>
    set({
      streamingMode: value,
    }),

  appendMessage: (conversationId, message) =>
    set({
      conversations: get().conversations.map((c) =>
        c.id === conversationId
          ? {
              ...c,
              updatedAt: new Date().toISOString(),
              messages: [...c.messages, message],
            }
          : c
      ),
    }),

  updateMessage: (
    conversationId,
    messageId,
    patch
  ) =>
    set({
      conversations: get().conversations.map((c) =>
        c.id !== conversationId
          ? c
          : {
              ...c,
              updatedAt: new Date().toISOString(),
              messages: c.messages.map((m) =>
                m.id === messageId
                  ? {
                      ...m,
                      ...patch,
                    }
                  : m
              ),
            }
      ),
    }),

  renameConversation: (
    conversationId,
    title
  ) =>
    set({
      conversations: get().conversations.map((c) =>
        c.id === conversationId
          ? {
              ...c,
              title,
            }
          : c
      ),
    }),

  renameFromFirstMessage: (
    conversationId,
    text
  ) =>
    set({
      conversations: get().conversations.map((c) =>
        c.id === conversationId &&
        c.title === "New conversation"
          ? {
              ...c,
              title: text.slice(0, 48),
            }
          : c
      ),
    }),
}));
import type { AssistantChatResponse, StreamEvent } from "@/types/api";

export type ChatRole = "user" | "assistant";

export interface ChatMessage {
  id: string;
  role: ChatRole;
  content: string;
  createdAt: string;
  streaming?: boolean;
  response?: AssistantChatResponse;
  executionEvents?: StreamEvent[];
  error?: string;
}

export interface Conversation {
  id: string;
  title: string;
  pinned: boolean;
  updatedAt: string;
  messages: ChatMessage[];
}

export type AsyncStatus = "idle" | "loading" | "success" | "error";

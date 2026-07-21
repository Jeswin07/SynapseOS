import { apiClient } from "@/services/apiClient";

export interface ConversationCreateRequest {
  dataset_version_id: string;
  title?: string;
}

export interface ConversationResponse {
  id: string;
  tenant_id: string;
  user_id: string;
  dataset_version_id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface ConversationUpdateRequest {
  title: string;
}

export const conversationService = {
  list() {
    return apiClient
      .get<ConversationResponse[]>("/conversations")
      .then((r) => r.data);
  },

  get(id: string) {
    return apiClient
      .get<ConversationResponse>(`/conversations/${id}`)
      .then((r) => r.data);
  },

  create(payload: ConversationCreateRequest) {
    return apiClient
      .post<ConversationResponse>("/conversations", payload)
      .then((r) => r.data);
  },

  update(id: string, payload: ConversationUpdateRequest) {
    return apiClient
      .patch<ConversationResponse>(`/conversations/${id}`, payload)
      .then((r) => r.data);
  },

  delete(id: string) {
    return apiClient.delete(`/conversations/${id}`);
  },
};
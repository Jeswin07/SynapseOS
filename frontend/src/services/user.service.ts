import { apiClient } from "@/services/apiClient";
import type { CreateUserRequest, UserResponse } from "@/types/api";

export const userService = {
  list() {
    return apiClient.get<UserResponse[]>("/users/").then((r) => r.data);
  },
  create(payload: CreateUserRequest) {
    return apiClient.post<UserResponse>("/users/", payload).then((r) => r.data);
  },
  // NOTE: backend does not expose PATCH/DELETE for users yet (edit role,
  // deactivate). TODO: backend — UI ships read-only + create until available.
};

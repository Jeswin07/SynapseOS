import { apiClient } from "@/services/apiClient";
import type { RegisterRequest, RegisterResponse, TokenResponse } from "@/types/api";

export const authService = {
  register(payload: RegisterRequest) {
    return apiClient.post<RegisterResponse>("/auth/register", payload).then((r) => r.data);
  },

  // Backend expects OAuth2PasswordRequestForm (application/x-www-form-urlencoded).
  login(email: string, password: string) {
    const form = new URLSearchParams();
    form.set("username", email);
    form.set("password", password);
    return apiClient
      .post<TokenResponse>("/auth/login", form, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      })
      .then((r) => r.data);
  },

  // NOTE: The backend defines RefreshTokenRequest/LogoutRequest schemas but does not
  // currently expose /auth/refresh or /auth/logout routes. Session end is handled
  // client-side only until those endpoints are wired up server-side. TODO: backend.
};

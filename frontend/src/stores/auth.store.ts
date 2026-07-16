import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { UserRole } from "@/types/api";

interface AuthState {
  accessToken: string | null;
  refreshToken: string | null;
  userId: string | null;
  role: UserRole | null;
  fullName: string | null;
  email: string | null;
  setSession: (session: {
    accessToken: string;
    refreshToken: string;
    userId: string;
    role: string;
    fullName?: string;
    email?: string;
  }) => void;
  clearSession: () => void;
  isAuthenticated: () => boolean;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      accessToken: null,
      refreshToken: null,
      userId: null,
      role: null,
      fullName: null,
      email: null,
      setSession: ({ accessToken, refreshToken, userId, role, fullName, email }) =>
        set({
          accessToken,
          refreshToken,
          userId,
          role: role as UserRole,
          fullName: fullName ?? get().fullName,
          email: email ?? get().email,
        }),
      clearSession: () =>
        set({
          accessToken: null,
          refreshToken: null,
          userId: null,
          role: null,
          fullName: null,
          email: null,
        }),
      isAuthenticated: () => Boolean(get().accessToken),
    }),
    { name: "synapseos-auth" }
  )
);

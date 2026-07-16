import { useMutation } from "@tanstack/react-query";
import { authService } from "@/services/auth.service";
import { tenantService } from "@/services/tenant.service";
import { useAuthStore } from "@/stores/auth.store";
import type { RegisterRequest } from "@/types/api";

export function useLogin() {
  const setSession = useAuthStore((s) => s.setSession);

  return useMutation({
    mutationFn: ({ email, password }: { email: string; password: string }) =>
      authService.login(email, password),
    onSuccess: (data, variables) => {
      setSession({
        accessToken: data.access_token,
        refreshToken: data.refresh_token,
        userId: data.user_id,
        role: data.role,
        email: variables.email,
      });
    },
  });
}

export function useRegister() {
  return useMutation({
    mutationFn: (payload: RegisterRequest) => authService.register(payload),
  });
}

export function useCreateTenant() {
  return useMutation({
    mutationFn: tenantService.create,
  });
}

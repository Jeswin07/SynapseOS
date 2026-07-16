import axios, { AxiosError, type InternalAxiosRequestConfig } from "axios";
import { useAuthStore } from "@/stores/auth.store";
import type { ApiErrorBody } from "@/types/api";

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60_000,
});

apiClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = useAuthStore.getState().accessToken;
  if (token) {
    config.headers.set("Authorization", `Bearer ${token}`);
  }
  return config;
});

export class ApiError extends Error {
  status: number;
  detail: string;

  constructor(status: number, detail: string) {
    super(detail);
    this.status = status;
    this.detail = detail;
  }
}

function extractDetail(body: ApiErrorBody | undefined, fallback: string): string {
  if (!body?.detail) return fallback;
  if (typeof body.detail === "string") return body.detail;
  if (Array.isArray(body.detail)) {
    return body.detail.map((d) => d.msg).join(", ");
  }
  return fallback;
}

const STATUS_MESSAGES: Record<number, string> = {
  400: "The request could not be processed. Please check your input.",
  401: "Your session has expired. Please sign in again.",
  403: "You don't have permission to perform this action.",
  404: "The requested resource could not be found.",
  422: "Some fields need your attention.",
  500: "Something went wrong on our end. Please try again shortly.",
};

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiErrorBody>) => {
    const status = error.response?.status ?? 0;
    const fallback = STATUS_MESSAGES[status] ?? "Unable to reach SynapseOS. Please check your connection.";
    const detail = extractDetail(error.response?.data, fallback);

    if (status === 401) {
      useAuthStore.getState().clearSession();
    }

    return Promise.reject(new ApiError(status, detail));
  }
);

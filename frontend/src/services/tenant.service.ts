import { apiClient } from "@/services/apiClient";
import type { TenantCreate, TenantResponse } from "@/types/api";

export const tenantService = {
  create(payload: TenantCreate) {
    return apiClient
      .post<{ tenant_id: string; company_name: string }>("/tenants/", payload)
      .then((r) => r.data);
  },
  // NOTE: no GET /tenants endpoint exposed by backend for reading the current
  // tenant's profile (used on Settings > Tenant). TODO: backend.
};
export type { TenantResponse };

import { apiClient } from "@/services/apiClient";
import type { RiskResponse } from "@/types/api";

export const riskService = {
  analyze() {
    return apiClient.get<RiskResponse>("/risks/analyze").then((r) => r.data);
  },
};

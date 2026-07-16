import { apiClient } from "@/services/apiClient";
import type { AnalyticsResult } from "@/types/api";

export const analyticsService = {
  run(datasetVersionId: string) {
    return apiClient
      .post<AnalyticsResult>("/analytics/run", { dataset_version_id: datasetVersionId })
      .then((r) => r.data);
  },
};

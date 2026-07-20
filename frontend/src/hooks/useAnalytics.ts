import { useMutation, useQuery } from "@tanstack/react-query";
import { analyticsService } from "@/services/analytics.service";
import type { AnalyticsRequest } from "@/types/api";

export function useRunAnalytics(datasetVersionId?: string) {
  return useQuery({
    queryKey: ["analytics", datasetVersionId],

    queryFn: () =>
      analyticsService.run({
        dataset_version_id: datasetVersionId!,
      }),

    enabled: Boolean(datasetVersionId),
  });
}

export function useRunAnalyticsMutation() {
  return useMutation({
    mutationFn: (request: AnalyticsRequest) =>
      analyticsService.run(request),
  });
}

export function useAnalyticsFilterOptions(
  datasetVersionId?: string,
) {
  return useQuery({
    queryKey: [
      "analytics-filter-options",
      datasetVersionId,
    ],

    queryFn: () =>
      analyticsService.getFilterOptions(
        datasetVersionId!,
      ),

    enabled: Boolean(datasetVersionId),
  });
}
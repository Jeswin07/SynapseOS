import { useMutation, useQuery } from "@tanstack/react-query";
import { analyticsService } from "@/services/analytics.service";

export function useRunAnalytics(datasetVersionId?: string) {
  return useQuery({
    queryKey: ["analytics", datasetVersionId],
    queryFn: () => analyticsService.run(datasetVersionId!),
    enabled: Boolean(datasetVersionId),
  });
}

export function useRunAnalyticsMutation() {
  return useMutation({
    mutationFn: (datasetVersionId: string) => analyticsService.run(datasetVersionId),
  });
}

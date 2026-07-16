import { useMutation, useQuery } from "@tanstack/react-query";
import { predictionService } from "@/services/prediction.service";
import type { PredictionType } from "@/types/api";

export function usePredictionHistory() {
  return useQuery({ queryKey: ["predictions", "history"], queryFn: predictionService.history });
}

export function useRunPrediction() {
  return useMutation({
    mutationFn: ({ datasetVersionId, predictionType }: { datasetVersionId: string; predictionType: PredictionType }) =>
      predictionService.run(datasetVersionId, predictionType),
  });
}

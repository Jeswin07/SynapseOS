import { apiClient } from "@/services/apiClient";
import type { PredictionHistoryItem, PredictionResult, PredictionType } from "@/types/api";

export const predictionService = {
  run(datasetVersionId: string, predictionType: PredictionType) {
    return apiClient
      .post<PredictionResult>("/predictions/run", {
        dataset_version_id: datasetVersionId,
        prediction_type: predictionType,
      })
      .then((r) => r.data);
  },
  history() {
    return apiClient.get<PredictionHistoryItem[]>("/predictions/history").then((r) => r.data);
  },
};

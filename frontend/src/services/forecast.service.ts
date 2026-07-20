import { apiClient } from "@/services/apiClient";
import type {
  ForecastPredictResponse,
  TrainForecastRequest,
  TrainForecastResponse,
} from "@/types/api";

export const forecastService = {
  train(payload: TrainForecastRequest) {
    return apiClient
      .post<TrainForecastResponse>("/forecast/train", payload)
      .then((r) => r.data);
  },

  predict(forecastId: string, periods = 30) {
    return apiClient
      .post<ForecastPredictResponse>("/forecast/predict", {
        forecast_id: forecastId,
        periods,
      })
      .then((r) => r.data);
  },
};
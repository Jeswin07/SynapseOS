import { useMutation } from "@tanstack/react-query";
import { forecastService } from "@/services/forecast.service";
import type { TrainForecastRequest } from "@/types/api";

export function useTrainForecast() {
  return useMutation({
    mutationFn: (payload: TrainForecastRequest) => forecastService.train(payload),
  });
}

export function usePredictForecast() {
  return useMutation({
    mutationFn: ({ forecastId, periods }: { forecastId: string; periods?: number }) =>
      forecastService.predict(forecastId, periods),
  });
}

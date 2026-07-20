import { apiClient } from "@/services/apiClient";
import type {
  AnalyticsRequest,
  AnalyticsResult,
} from "@/types/api";

export interface FilterList {
  enabled: boolean;
  values: string[];
}

export interface DateFilter {
  enabled: boolean;
  min: string;
  max: string;
}

export interface RangeFilter {
  enabled: boolean;
  min: number;
  max: number;
}

export interface AnalyticsFilterOptions {
  date: DateFilter;

  states: FilterList;
  categories: FilterList;
  brands: FilterList;

  revenue: RangeFilter;
  review_score: RangeFilter;
}

export const analyticsService = {
  async run(
    request: AnalyticsRequest,
  ): Promise<AnalyticsResult> {
    const { data } =
      await apiClient.post<AnalyticsResult>(
        "/analytics/run",
        request,
      );

    return data;
  },

  async getFilterOptions(
    datasetVersionId: string,
  ): Promise<AnalyticsFilterOptions> {
    const { data } =
      await apiClient.get<AnalyticsFilterOptions>(
        `/analytics/${datasetVersionId}/filter-options`,
      );

    return data;
  },
};
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { BarChart3, Play, Loader2 } from "lucide-react";

import { PageHeader } from "@/components/common/PageHeader";
import { DatasetVersionSelect } from "@/components/common/DatasetVersionSelect";
import { ChartSkeleton, CardGridSkeleton } from "@/components/common/LoadingSkeleton";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

import { AnalyticsResultView } from "@/features/analytics/components/AnalyticsResultView";
import { AnalyticsFilters } from "@/features/analytics/components/AnalyticsFilters";

import {
  useAnalyticsFilterOptions,
  useRunAnalyticsMutation,
} from "@/hooks/useAnalytics";

import { ApiError } from "@/services/apiClient";
import type { DatasetFilters } from "@/types/api";

import { toast } from "sonner";

export default function AnalyticsPage() {
  const [searchParams] = useSearchParams();

  const [datasetId, setDatasetId] = useState<string | null>(null);

  const [versionId, setVersionId] = useState<string | null>(
    searchParams.get("dataset_version_id")
  );

  const [filters, setFilters] = useState<DatasetFilters>({});

  const runAnalytics = useRunAnalyticsMutation();

  const filterOptions = useAnalyticsFilterOptions(
    versionId ?? undefined,
  );

  useEffect(() => {
    const paramVersion = searchParams.get("dataset_version_id");

    if (paramVersion) {
      setVersionId(paramVersion);
    }
  }, [searchParams]);

  function handleRun() {
    if (!versionId) return;

    runAnalytics.mutate(
      {
        dataset_version_id: versionId,
        filters,
      },
      {
        onError: (err) => {
          toast.error(
            err instanceof ApiError
              ? err.detail
              : "Analytics run failed."
          );
        },
      }
    );
  }

  return (
    <div>
      <PageHeader
        title="Analytics"
        description="Run business analytics across revenue, customers, products, and operations."
        actions={
          <Button
            onClick={handleRun}
            disabled={!versionId || runAnalytics.isPending}
          >
            {runAnalytics.isPending ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Play className="h-4 w-4" />
            )}

            Run Analytics
          </Button>
        }
      />

      <Card className="mb-6">
        <CardContent className="space-y-6 p-5">
          <DatasetVersionSelect
            datasetId={datasetId}
            versionId={versionId}
            onDatasetChange={(id) => {
              setDatasetId(id);
              setVersionId(null);
            }}
            onVersionChange={setVersionId}
          />

          <AnalyticsFilters
            filters={filters}
            setFilters={setFilters}
            filterOptions={filterOptions.data}
            isLoading={filterOptions.isLoading}
          />
        </CardContent>
      </Card>

      {runAnalytics.isPending ? (
        <div className="space-y-6">
          <CardGridSkeleton />
          <ChartSkeleton />
        </div>
      ) : runAnalytics.isError ? (
        <ErrorState onRetry={handleRun} />
      ) : runAnalytics.data ? (
        <AnalyticsResultView
          result={runAnalytics.data}
        />
      ) : (
        <EmptyState
          icon={BarChart3}
          title="Select a dataset version and run analytics"
          description="Choose a dataset version, optionally apply filters, then run analytics to generate business insights."
        />
      )}
    </div>
  );
}
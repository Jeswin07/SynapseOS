import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { toast } from "sonner";
import { TrendingUp, Loader2, Sparkles } from "lucide-react";
import { PageHeader } from "@/components/common/PageHeader";
import { DatasetVersionSelect } from "@/components/common/DatasetVersionSelect";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { EmptyState } from "@/components/common/EmptyState";
import { ErrorState } from "@/components/common/ErrorState";
import { ChartSkeleton } from "@/components/common/LoadingSkeleton";
import { ForecastChart } from "@/features/forecasting/components/ForecastChart";
import { useTrainForecast, usePredictForecast } from "@/hooks/useForecast";
import { ApiError } from "@/services/apiClient";
import { ForecastSummaryCards } from "@/features/forecasting/components/ForecastSummaryCards";

export default function ForecastingPage() {
  const [searchParams] = useSearchParams();
  const [datasetId, setDatasetId] = useState<string | null>(null);
  const [versionId, setVersionId] = useState<string | null>(searchParams.get("dataset_version_id"));
  const [query, setQuery] = useState("forecast revenue");
  const [periods, setPeriods] = useState(30);
  const [forecastId, setForecastId] = useState<string | null>(null);

  const trainForecast = useTrainForecast();
  const predictForecast = usePredictForecast();

  useEffect(() => {
    const paramVersion = searchParams.get("dataset_version_id");
    if (paramVersion) setVersionId(paramVersion);
  }, [searchParams]);

  function handleTrain() {
    if (!versionId) return;

    trainForecast.mutate(
      {
        dataset_version_id: versionId,
        query,
      },
      {
        onSuccess: (data) => {
          setForecastId(data.forecast_id);
          toast.success("Forecast model trained successfully.");
        },
        onError: (err) => {
          toast.error(
            err instanceof ApiError
              ? err.detail
              : "Forecast training failed."
          );
        },
      }
    );
  }

  function handlePredict() {
    if (!forecastId) return;
    predictForecast.mutate(
      { forecastId, periods },
      {
        onError: (err) => {
          toast.error(err instanceof ApiError ? err.detail : "Prediction failed.");
        },
      }
    );
  }

  return (
    <div>
      <PageHeader
        title="Forecasting"
        description="Train time-series forecasting models and project future values."
      />

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle>1. Select data</CardTitle>
            <CardDescription className="mt-1">Choose the dataset version to train on.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <DatasetVersionSelect
              datasetId={datasetId}
              versionId={versionId}
              onDatasetChange={(id) => {
                setDatasetId(id);
                setVersionId(null);
                setForecastId(null);
              }}
              onVersionChange={(id) => {
                setVersionId(id);
                setForecastId(null);
              }}
            />
            <div className="space-y-1.5">
              <Label htmlFor="query">Business Question</Label>

              <Input
                id="query"
                placeholder="Forecast monthly revenue"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />

              <p className="text-xs text-muted-foreground">
                Examples: Forecast revenue, Forecast daily orders,
                Forecast monthly payment value.
              </p>
            </div>
            <Button className="w-full" onClick={handleTrain} disabled={!versionId || trainForecast.isPending}>
              {trainForecast.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
              Build forecast model
            </Button>
          </CardContent>
        </Card>

        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle>2. Generate forecast</CardTitle>
            <CardDescription className="mt-1">Project values for upcoming periods.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-1.5">
              <Label htmlFor="periods">Periods to forecast</Label>
              <select
                className="w-full rounded-md border bg-background px-3 py-2"
                value={periods}
                onChange={(e) => setPeriods(Number(e.target.value))}
              >
                <option value={7}>7 Days</option>
                <option value={30}>30 Days</option>
                <option value={90}>90 Days</option>
                <option value={180}>180 Days</option>
                <option value={365}>365 Days</option>
              </select>
            </div>
            <Button
              className="w-full"
              variant="outline"
              onClick={handlePredict}
              disabled={!forecastId || predictForecast.isPending}
            >
              {predictForecast.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <TrendingUp className="h-4 w-4" />}
              Generate Forecast
            </Button>
            {!forecastId && (
              <p className="text-xs text-muted-foreground">Train a model first to enable predictions.</p>
            )}
          </CardContent>
        </Card>

        <div className="lg:col-span-1" />
      </div>

      <div className="mt-6">
        {predictForecast.isPending ? (
          <ChartSkeleton />
        ) : predictForecast.isError ? (
          <ErrorState onRetry={handlePredict} />
        ) : predictForecast.data ? (
          <>
            <ForecastSummaryCards
              summary={predictForecast.data.summary}
              evaluation={predictForecast.data.evaluation}
            />

            <div className="mt-6">
              <ForecastChart
                points={predictForecast.data.forecast}
              />
            </div>
          </>
        ) : (
          <EmptyState
            icon={TrendingUp}
            title="No forecast generated yet"
            description="Train a model and generate predictions to see the projected trend."
          />
        )}
      </div>
    </div>
  );
}

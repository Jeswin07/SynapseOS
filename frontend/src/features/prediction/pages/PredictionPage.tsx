import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { toast } from "sonner";
import { Target, Loader2, Play, History } from "lucide-react";
import { PageHeader } from "@/components/common/PageHeader";
import { DatasetVersionSelect } from "@/components/common/DatasetVersionSelect";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { EmptyState } from "@/components/common/EmptyState";
import { ErrorState } from "@/components/common/ErrorState";
import { CardGridSkeleton, TableSkeleton } from "@/components/common/LoadingSkeleton";
import { PredictionResultView } from "@/features/prediction/components/PredictionResultView";
import { useRunPrediction, usePredictionHistory } from "@/hooks/usePrediction";
import { ApiError } from "@/services/apiClient";
import type { PredictionType } from "@/types/api";
import { titleCase, formatPercent } from "@/utils/format";

const PREDICTION_TYPES: { value: PredictionType; label: string }[] = [
  { value: "customer_churn", label: "Customer churn" },
  { value: "delivery_delay", label: "Delivery delay" },
];

export default function PredictionPage() {
  const [searchParams] = useSearchParams();
  const [datasetId, setDatasetId] = useState<string | null>(null);
  const [versionId, setVersionId] = useState<string | null>(searchParams.get("dataset_version_id"));
  const [predictionType, setPredictionType] = useState<PredictionType>("customer_churn");

  const runPrediction = useRunPrediction();
  const history = usePredictionHistory();

  useEffect(() => {
    const paramVersion = searchParams.get("dataset_version_id");
    if (paramVersion) setVersionId(paramVersion);
  }, [searchParams]);

  function handleRun() {
    if (!versionId) return;
    runPrediction.mutate(
      { datasetVersionId: versionId, predictionType },
      {
        onError: (err) => {
          toast.error(err instanceof ApiError ? err.detail : "Prediction run failed.");
        },
      }
    );
  }

  return (
    <div>
      <PageHeader
        title="Prediction"
        description="Predict customer churn and delivery delay risk with entity-level detail."
      />

      <Tabs defaultValue="run">
        <TabsList>
          <TabsTrigger value="run">
            <Play className="mr-1.5 h-3.5 w-3.5" /> Run prediction
          </TabsTrigger>
          <TabsTrigger value="history">
            <History className="mr-1.5 h-3.5 w-3.5" /> History
          </TabsTrigger>
        </TabsList>

        <TabsContent value="run" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Configure prediction</CardTitle>
              <CardDescription className="mt-1">Select data and a prediction model to run.</CardDescription>
            </CardHeader>
            <CardContent className="flex flex-col gap-4">
              <DatasetVersionSelect
                datasetId={datasetId}
                versionId={versionId}
                onDatasetChange={(id) => {
                  setDatasetId(id);
                  setVersionId(null);
                }}
                onVersionChange={setVersionId}
              />
              <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
                <div className="w-full sm:w-64">
                  <Select value={predictionType} onValueChange={(v) => setPredictionType(v as PredictionType)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {PREDICTION_TYPES.map((t) => (
                        <SelectItem key={t.value} value={t.value}>
                          {t.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <Button onClick={handleRun} disabled={!versionId || runPrediction.isPending}>
                  {runPrediction.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4" />}
                  Run prediction
                </Button>
              </div>
            </CardContent>
          </Card>

          {runPrediction.isPending ? (
            <CardGridSkeleton count={3} />
          ) : runPrediction.isError ? (
            <ErrorState onRetry={handleRun} />
          ) : runPrediction.data ? (
            <PredictionResultView result={runPrediction.data} />
          ) : (
            <EmptyState
              icon={Target}
              title="No prediction run yet"
              description="Configure a dataset and prediction type above, then run to see results."
            />
          )}
        </TabsContent>

        <TabsContent value="history">
          {history.isLoading ? (
            <TableSkeleton />
          ) : history.isError ? (
            <ErrorState onRetry={() => history.refetch()} />
          ) : history.data && history.data.length > 0 ? (
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {history.data.map((item) => (
                <Card key={item.id}>
                  <CardContent className="space-y-2 p-4">
                    <div className="flex items-center justify-between">
                      <Badge variant="secondary">{titleCase(item.prediction_type)}</Badge>
                      <span className="text-xs text-muted-foreground">
                        {item.result.summary.total_entities} entities
                      </span>
                    </div>
                    <p className="text-sm text-foreground">
                      {formatPercent(item.result.summary.average_probability, false)} avg. probability
                    </p>
                    <p className="text-xs text-muted-foreground">{item.result.summary.high_risk_entities} high-risk entities</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <EmptyState icon={History} title="No prediction history" description="Runs you complete will appear here." />
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}

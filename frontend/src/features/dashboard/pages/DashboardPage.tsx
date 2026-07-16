import { Link } from "react-router-dom";
import { Database, Target, ShieldAlert, Sparkles, ArrowRight, Info } from "lucide-react";
import { PageHeader } from "@/components/common/PageHeader";
import { MetricCard } from "@/components/common/MetricCard";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { StatusBadge } from "@/components/common/StatusBadge";
import { CardGridSkeleton, TableSkeleton } from "@/components/common/LoadingSkeleton";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";
import { useDatasets } from "@/hooks/useDatasets";
import { usePredictionHistory } from "@/hooks/usePrediction";
import { useRiskAnalysis } from "@/hooks/useRisk";
import { titleCase, formatRelativeTime, formatPercent } from "@/utils/format";

export default function DashboardPage() {
  const datasets = useDatasets();
  const predictions = usePredictionHistory();
  const risk = useRiskAnalysis();

  const isLoading = datasets.isLoading || predictions.isLoading || risk.isLoading;

  return (
    <div>
      <PageHeader
        title="Dashboard"
        description="A live snapshot of your enterprise data, predictions, and risk posture."
        actions={
          <Button asChild>
            <Link to="/assistant">
              <Sparkles className="h-4 w-4" /> Ask the assistant
            </Link>
          </Button>
        }
      />

      {isLoading ? (
        <CardGridSkeleton />
      ) : (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <MetricCard label="Datasets" value={String(datasets.data?.length ?? 0)} icon={Database} />
          <MetricCard
            label="Prediction runs"
            value={String(predictions.data?.length ?? 0)}
            icon={Target}
          />
          <MetricCard
            label="Overall risk score"
            value={risk.data ? risk.data.overall_risk.toFixed(1) : "—"}
            icon={ShieldAlert}
          />
          <MetricCard
            label="Risk level"
            value={risk.data ? titleCase(risk.data.level) : "—"}
            icon={ShieldAlert}
          />
        </div>
      )}

      <div className="mt-6 grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader className="flex-row items-center justify-between space-y-0">
            <div>
              <CardTitle>Recent datasets</CardTitle>
              <CardDescription className="mt-1">The latest data sources connected to your workspace.</CardDescription>
            </div>
            <Button variant="ghost" size="sm" asChild>
              <Link to="/datasets">
                View all <ArrowRight className="h-3.5 w-3.5" />
              </Link>
            </Button>
          </CardHeader>
          <CardContent>
            {datasets.isLoading ? (
              <TableSkeleton rows={4} />
            ) : datasets.isError ? (
              <ErrorState onRetry={() => datasets.refetch()} />
            ) : datasets.data && datasets.data.length > 0 ? (
              <div className="space-y-1">
                {datasets.data.slice(0, 6).map((d) => (
                  <Link
                    key={d.id}
                    to={`/datasets/${d.id}`}
                    className="flex items-center justify-between rounded-lg px-3 py-2.5 text-sm transition-colors hover:bg-muted/50"
                  >
                    <div className="min-w-0">
                      <p className="truncate font-medium text-foreground">{d.name}</p>
                      <p className="truncate text-xs text-muted-foreground">
                        {titleCase(d.dataset_type)} · {titleCase(d.business_domain)}
                      </p>
                    </div>
                    <span className="shrink-0 text-xs text-muted-foreground">{formatRelativeTime(d.created_at)}</span>
                  </Link>
                ))}
              </div>
            ) : (
              <EmptyState
                icon={Database}
                title="No datasets yet"
                description="Upload your first dataset to unlock analytics, forecasting, and predictions."
                actionLabel="Add dataset"
                onAction={() => (window.location.href = "/datasets")}
              />
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Top risks</CardTitle>
            <CardDescription className="mt-1">From the latest enterprise risk analysis.</CardDescription>
          </CardHeader>
          <CardContent>
            {risk.isLoading ? (
              <TableSkeleton rows={3} />
            ) : risk.isError ? (
              <ErrorState onRetry={() => risk.refetch()} />
            ) : risk.data && risk.data.risks.length > 0 ? (
              <div className="space-y-3">
                {risk.data.risks.slice(0, 5).map((r, idx) => (
                  <div key={idx} className="flex items-start justify-between gap-2 text-sm">
                    <div className="min-w-0">
                      <p className="truncate font-medium text-foreground">{titleCase(r.type)}</p>
                      <p className="text-xs text-muted-foreground">Score {r.score.toFixed(1)}</p>
                    </div>
                    <StatusBadge status={r.severity} />
                  </div>
                ))}
              </div>
            ) : (
              <EmptyState title="No risks detected" description="Your enterprise risk profile is currently clear." />
            )}
          </CardContent>
        </Card>
      </div>

      <div className="mt-6">
        <Card>
          <CardHeader className="flex-row items-center justify-between space-y-0">
            <div>
              <CardTitle>Recent prediction runs</CardTitle>
              <CardDescription className="mt-1">Customer churn and delivery delay predictions.</CardDescription>
            </div>
            <Button variant="ghost" size="sm" asChild>
              <Link to="/prediction">
                View all <ArrowRight className="h-3.5 w-3.5" />
              </Link>
            </Button>
          </CardHeader>
          <CardContent>
            {predictions.isLoading ? (
              <TableSkeleton rows={3} />
            ) : predictions.isError ? (
              <ErrorState onRetry={() => predictions.refetch()} />
            ) : predictions.data && predictions.data.length > 0 ? (
              <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
                {predictions.data.slice(0, 6).map((p) => (
                  <div key={p.id} className="rounded-lg border border-border p-3">
                    <div className="flex items-center justify-between">
                      <Badge variant="secondary">{titleCase(p.prediction_type)}</Badge>
                      <span className="text-xs text-muted-foreground">
                        {p.result.summary.total_entities} entities
                      </span>
                    </div>
                    <p className="mt-2 text-sm text-foreground">
                      {formatPercent(p.result.summary.average_probability, false)} avg. probability
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {p.result.summary.high_risk_entities} high-risk
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <EmptyState
                icon={Target}
                title="No predictions yet"
                description="Run your first churn or delivery-delay prediction from the Prediction workspace."
                actionLabel="Go to Prediction"
                onAction={() => (window.location.href = "/prediction")}
              />
            )}
          </CardContent>
        </Card>
      </div>

      <p className="mt-6 flex items-start gap-2 text-xs text-muted-foreground">
        <Info className="mt-0.5 h-3.5 w-3.5 shrink-0" />
        This dashboard composes data from the Datasets, Predictions, and Risk APIs. A dedicated summary endpoint
        is not yet exposed by the backend, so figures reflect what those APIs currently return.
      </p>
    </div>
  );
}

import { Users, AlertTriangle, Percent } from "lucide-react";
import { MetricCard } from "@/components/common/MetricCard";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { DataTable, type DataTableColumn } from "@/components/common/DataTable";
import { StatusBadge } from "@/components/common/StatusBadge";
import type { EntityPrediction, PredictionResult } from "@/types/api";
import { formatPercent } from "@/utils/format";

export function PredictionResultView({
  result,
}: {
  result: PredictionResult;
}) {
  const columns: DataTableColumn<EntityPrediction>[] = [
    {
      key: "entity_id",
      header: "Entity",
      render: (r) => (
        <span className="font-medium">{r.entity_id}</span>
      ),
      sortValue: (r) => r.entity_id,
    },
    {
      key: "probability",
      header: "Probability",
      render: (r) => formatPercent(r.probability, false),
      sortValue: (r) => r.probability,
    },
    {
      key: "level",
      header: "Risk level",
      render: (r) => <StatusBadge status={r.level} />,
      sortValue: (r) => r.level,
    },
    {
      key: "drivers",
      header: "Key drivers",
      render: (r) => (
        <span className="text-sm text-muted-foreground">
          {r.drivers.slice(0, 2).join(", ") || "—"}
        </span>
      ),
    },
  ];

  const metrics = (result.metadata as any)?.metrics;
  const featureImportance =
    ((result.metadata as any)?.feature_importance as any[]) ?? [];

  return (
    <div className="space-y-6">
      {/* Summary */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <MetricCard
          label="Entities analyzed"
          value={String(result.summary.total_entities)}
          icon={Users}
        />

        <MetricCard
          label="High risk"
          value={String(result.summary.high_risk_entities)}
          icon={AlertTriangle}
        />

        <MetricCard
          label="Avg. probability"
          value={formatPercent(result.summary.average_probability, false)}
          icon={Percent}
        />
      </div>

      {/* Model Evaluation */}
      {metrics && (
        <Card>
          <CardHeader>
            <CardTitle>Model Evaluation</CardTitle>
          </CardHeader>

          <CardContent>
            <div className="grid grid-cols-2 gap-4 md:grid-cols-5">
              <MetricCard
                label="Accuracy"
                value={formatPercent(metrics.accuracy, false)}
              />

              <MetricCard
                label="Precision"
                value={formatPercent(metrics.precision, false)}
              />

              <MetricCard
                label="Recall"
                value={formatPercent(metrics.recall, false)}
              />

              <MetricCard
                label="F1 Score"
                value={formatPercent(metrics.f1_score, false)}
              />

              <MetricCard
                label="ROC AUC"
                value={formatPercent(metrics.roc_auc, false)}
              />
            </div>
          </CardContent>
        </Card>
      )}

      {/* Feature Importance */}
      {featureImportance.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Top Model Features</CardTitle>
          </CardHeader>

          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="border-b">
                  <tr>
                    <th className="py-2 text-left">Feature</th>
                    <th className="py-2 text-right">Importance</th>
                  </tr>
                </thead>

                <tbody>
                  {featureImportance.map((item) => (
                    <tr
                      key={item.feature}
                      className="border-b last:border-0"
                    >
                      <td className="py-2">{item.feature}</td>

                      <td className="py-2 text-right font-medium">
                        {item.importance.toFixed(4)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Recommendations */}
      {result.recommendations.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Recommendations</CardTitle>
          </CardHeader>

          <CardContent>
            <ul className="space-y-2">
              {result.recommendations.map((rec, idx) => (
                <li
                  key={idx}
                  className="flex gap-2 text-sm text-foreground"
                >
                  <span className="text-primary">•</span>
                  {rec}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      {/* Entity Predictions */}
      <Card>
        <CardHeader>
          <CardTitle>Entity-level Predictions</CardTitle>
        </CardHeader>

        <CardContent>
          <DataTable
            columns={columns}
            data={result.predictions}
            rowKey={(r) => r.entity_id}
            searchFilter={(r, q) =>
              r.entity_id.toLowerCase().includes(q.toLowerCase())
            }
            searchPlaceholder="Search entities..."
            emptyTitle="No entity-level predictions"
          />
        </CardContent>
      </Card>
    </div>
  );
}
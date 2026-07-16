import { Users, AlertTriangle, Percent } from "lucide-react";
import { MetricCard } from "@/components/common/MetricCard";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { DataTable, type DataTableColumn } from "@/components/common/DataTable";
import { StatusBadge } from "@/components/common/StatusBadge";
import type { EntityPrediction, PredictionResult } from "@/types/api";
import { formatPercent } from "@/utils/format";

export function PredictionResultView({ result }: { result: PredictionResult }) {
  const columns: DataTableColumn<EntityPrediction>[] = [
    { key: "entity_id", header: "Entity", render: (r) => <span className="font-medium">{r.entity_id}</span>, sortValue: (r) => r.entity_id },
    {
      key: "probability",
      header: "Probability",
      render: (r) => formatPercent(r.probability, false),
      sortValue: (r) => r.probability,
    },
    { key: "level", header: "Risk level", render: (r) => <StatusBadge status={r.level} />, sortValue: (r) => r.level },
    {
      key: "drivers",
      header: "Key drivers",
      render: (r) => <span className="text-sm text-muted-foreground">{r.drivers.slice(0, 2).join(", ") || "—"}</span>,
    },
  ];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <MetricCard label="Entities analyzed" value={String(result.summary.total_entities)} icon={Users} />
        <MetricCard label="High risk" value={String(result.summary.high_risk_entities)} icon={AlertTriangle} />
        <MetricCard
          label="Avg. probability"
          value={formatPercent(result.summary.average_probability, false)}
          icon={Percent}
        />
      </div>

      {result.recommendations.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Recommendations</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {result.recommendations.map((rec, idx) => (
                <li key={idx} className="flex gap-2 text-sm text-foreground">
                  <span className="text-primary">•</span>
                  {rec}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Entity-level predictions</CardTitle>
        </CardHeader>
        <CardContent>
          <DataTable
            columns={columns}
            data={result.predictions}
            rowKey={(r) => r.entity_id}
            searchFilter={(r, q) => r.entity_id.toLowerCase().includes(q.toLowerCase())}
            searchPlaceholder="Search entities…"
            emptyTitle="No entity-level predictions"
          />
        </CardContent>
      </Card>
    </div>
  );
}

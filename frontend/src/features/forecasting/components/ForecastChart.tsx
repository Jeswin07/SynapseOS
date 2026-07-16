import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { ChartCard } from "@/components/common/ChartCard";
import type { ForecastPoint } from "@/types/api";
import { formatCompactNumber, formatDate } from "@/utils/format";

export function ForecastChart({ points }: { points: ForecastPoint[] }) {
  const data = points.map((p) => ({ ...p, dateLabel: formatDate(p.date) }));

  return (
    <ChartCard title="Forecast" description={`Projected values for the next ${points.length} periods`}>
      <ResponsiveContainer width="100%" height={320}>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="forecastFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="hsl(221 83% 45%)" stopOpacity={0.25} />
              <stop offset="95%" stopColor="hsl(221 83% 45%)" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
          <XAxis dataKey="dateLabel" tick={{ fontSize: 12 }} stroke="hsl(var(--muted-foreground))" />
          <YAxis tick={{ fontSize: 12 }} stroke="hsl(var(--muted-foreground))" tickFormatter={(v) => formatCompactNumber(v)} />
          <Tooltip contentStyle={{ borderRadius: 8, borderColor: "hsl(var(--border))", fontSize: 13 }} />
          <Area type="monotone" dataKey="upper" stroke="none" fill="hsl(221 83% 45%)" fillOpacity={0.08} />
          <Area type="monotone" dataKey="lower" stroke="none" fill="hsl(var(--background))" fillOpacity={1} />
          <Area
            type="monotone"
            dataKey="prediction"
            stroke="hsl(221 83% 45%)"
            strokeWidth={2}
            fill="url(#forecastFill)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}
